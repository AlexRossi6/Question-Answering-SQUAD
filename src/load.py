import json
import pandas as pd
from pathlib import Path


class LoadData_train():
    def __init__(self,
                 path_to_json_file: str,
                 checkpoint_path: str,
                 train_file: str = 'train.csv',
                 val_file: str = 'val.csv') -> None:
        """Load the data by flattening the json file and saving it.

        Args:
            path_to_json_file: path to the json file.
            checkpoint_path: path where to save the csv files.
            train_file: name of the train csv file that will be created.
            val_file: name of the val csv file that will be created.
        """

        self.path_to_json_file = path_to_json_file
        self.checkpoint_path = checkpoint_path

        self.train_file = train_file
        self.val_file = val_file

        self.data = self.load_data()

    def load_data(self):
        with open(self.path_to_json_file, 'r') as f:
            train_data = json.load(f)
        print(f'Flattening SQUAD {train_data["version"]}')
        train_data_flat, val_data_flat, errors = self.load_squad_data(train_data)
        print(f'\nErroneous Datapoints: {errors}')

        pd.DataFrame(train_data_flat).to_csv(Path(self.checkpoint_path) / Path(self.train_file), encoding='utf-8')

        pd.DataFrame(val_data_flat).to_csv(Path(self.checkpoint_path) / Path(self.val_file), encoding='utf-8')

    def load_squad_data(self, data, split=0.2):

        errors = 0
        flattened_data_train = []
        flattened_data_val = []

        train_range = len(data['data']) - (len(data['data']) * split)

        for i, article in enumerate(data["data"]):
            title = article.get("title", "").strip()
            for paragraph in article["paragraphs"]:
                context = paragraph["context"].strip()
                for qa in paragraph["qas"]:
                    question = qa["question"].strip()
                    id_ = qa["id"]

                    answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                    answers = [answer["text"].strip() for answer in qa["answers"]]

                    # Features currently used are "context", "question", and "answers".
                    # Others are extracted here for the ease of future expansions.
                    if i <= train_range:
                        flattened_data_train.append({"title": title,
                                                     "context": context,
                                                     "question": question,
                                                     "id": id_,
                                                     "answers": {
                                                         "answer_start": answer_starts,
                                                         "text": answers}
                                                     })
                    else:
                        flattened_data_val.append({"title": title,
                                                   "context": context,
                                                   "question": question,
                                                   "id": id_,
                                                   "answers": {
                                                       "answer_start": answer_starts,
                                                       "text": answers}
                                                   })

        return flattened_data_train, flattened_data_val, errors


class LoadData():
    def __init__(self,
                 path_to_json_file: str,
                 checkpoint_path: str,
                 test_file: str = 'test.csv') -> None:
        """Load the data by flattening the json file and saving it.

          Args:
              path_to_json_file: path to the json file.
              checkpoint_path: path where to save the csv files.
              test_file: name of the test csv file that will be created.
        """

        self.path_to_json_file = path_to_json_file
        self.checkpoint_path = checkpoint_path

        self.test_file = test_file

        self.data = self.load_data()

    def load_data(self):
        with open(self.path_to_json_file, 'r') as f:
            test_data = json.load(f)
        print(f'Flattening SQUAD {test_data["version"]}')
        test_data_flat, errors = self.load_squad_data(test_data)
        print(f'\nErroneous Datapoints: {errors}')

        pd.DataFrame(test_data_flat).to_csv(Path(self.checkpoint_path) / Path(self.test_file), encoding='utf-8')

    def load_squad_data(self, data):

        errors = 0
        flattened_data_test = []

        for i, article in enumerate(data["data"]):
            title = article.get("title", "").strip()
            for paragraph in article["paragraphs"]:
                context = paragraph["context"].strip()
                for qa in paragraph["qas"]:
                    question = qa["question"].strip()
                    id_ = qa["id"]

                    answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                    answers = [answer["text"].strip() for answer in qa["answers"]]

                    # Features currently used are "context", "question", and "answers".
                    # Others are extracted here for the ease of future expansions.
                    flattened_data_test.append({"title": title,
                                                "context": context,
                                                "question": question,
                                                "id": id_,
                                                "answers": {
                                                    "answer_start": answer_starts,
                                                    "text": answers}
                                                })

        return flattened_data_test, errors
