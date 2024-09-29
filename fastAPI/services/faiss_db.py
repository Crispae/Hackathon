import faiss
import numpy as np
import json
from typing import List
from mistralai import Mistral
import os
import base64


class DenseSearchFAISS:
    def __init__(
        self,
        embedding_model,
        api_key,
        dimension: int,
        base_path: str,
        prefix: str,
        suffix: str,
        index_file="index\\faiss_index.index",
        ids_file="index\\ids.json",
    ):
        self.index_file = index_file
        self.ids_file = ids_file
        self.base_path = base_path
        self.prefix = prefix
        self.suffix = suffix

        ## FAISS index
        try:
            self.index = faiss.read_index(self.index_file)
            self.ids = self._load_ids()
            print("FAISS index and IDs loaded from disk.")

        except Exception:
            # If index does not exist, create a new one
            self.index = faiss.IndexFlatL2(dimension)  # L2 distance based search
            self.ids = []
            print("Initialized a new FAISS index.")

        ## Embedding model
        self.embedding_model = embedding_model
        self.embedding_api_key = api_key
        self.embedding_model_client = Mistral(api_key=self.embedding_api_key)

    def _save_ids(self):
        """Save document IDs to disk."""
        with open(self.ids_file, "w") as f:
            json.dump(self.ids, f)

    def _load_ids(self):
        """Load document IDs from disk."""
        with open(self.ids_file, "r") as f:
            return json.load(f)

    def save_index(self):
        """Save the FAISS index and document IDs to disk."""
        faiss.write_index(self.index, self.index_file)
        self._save_ids()
        print(
            f"FAISS index saved to {self.index_file} and IDs saved to {self.ids_file}."
        )

    def add_documents(self, documents: List[str], ids: List[str]):
        # Fetch embeddings from the embedding model
        embeddings_batch_response = self.embedding_model_client.embeddings.create(
            model=self.embedding_model,
            inputs=documents,
        )

        embeddings_list = []
        for idx, id in enumerate(ids):
            embeddings = (
                embeddings_batch_response.dict().get("data")[idx].get("embedding")
            )
            embeddings_list.append(embeddings)
            self.ids.append(str(id))  # Store the document ID

        # Convert embeddings list to NumPy array for FAISS
        embeddings_np = np.array(embeddings_list).astype("float32")

        # Add the embeddings to the FAISS index
        self.index.add(embeddings_np)

        self.save_index()

    def search(self, query: str, k=30, encoded=False):
        # Get the embedding for the query text
        query_embedding_response = self.embedding_model_client.embeddings.create(
            model=self.embedding_model,
            inputs=[query],
        )
        query_embedding = (
            query_embedding_response.dict().get("data")[0].get("embedding")
        )

        # Convert the query embedding to a NumPy array
        query_embedding_np = np.array([query_embedding]).astype("float32")

        # Search for the top-k most similar embeddings
        distances, indices = self.index.search(query_embedding_np, k)

        # Map the indices to the corresponding document IDs
        results = [(self.ids[i], distances[0][idx]) for idx, i in enumerate(indices[0])]
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        if encoded:
            ## Getting paths
            paths = DenseSearchFAISS.score_to_path(
                scores=sorted_results,
                base_path=self.base_path,
                prefix=self.prefix,
                suffix=self.suffix,
                with_score=True,
            )

            ## Generate base 64 images from paths
            encoded_path = DenseSearchFAISS.file_to_data_url(file_paths=paths)
            return encoded_path

        else:
            return sorted_results

    @staticmethod
    def _score_to_path_with_score(
        scores,
        paths,
    ):
        if len(paths) == len(scores):
            scores_list = [score[1] for score in scores]
            return list(zip(paths, scores_list))
        else:
            raise ValueError("Number of paths and scores should be equal")

    @staticmethod
    def score_to_path(
        scores,
        base_path,
        prefix,
        suffix,
        with_score=True,
    ):
        paths = []
        for score in scores:
            path = os.path.join(
                base_path,
                f"{prefix}_{score[0]}.{suffix}",
            )
            paths.append(path)
        ## appending score with path
        if with_score:
            return DenseSearchFAISS._score_to_path_with_score(
                scores=scores,
                paths=paths,
            )
        else:
            return paths

    @staticmethod
    def file_to_data_url(file_paths: List):
        """
        Convert a local image file to a data URL.
        """

        encoded_response = []

        for file_path in file_paths:
            path, score = file_path

            with open(path, "rb") as image_file:
                ## Encoding url to base64
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

                ## Getting mime type
                _, extension = os.path.splitext(path)
                mime_type = f"image/{extension[1:].lower()}"

                ## Encoded image
                encoding = f"data:{mime_type};base64,{encoded_string}"

                encoded_response.append({"encoding": encoding, "score": float(score)})

        return encoded_response
