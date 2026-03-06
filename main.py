import argparse
import json
import os

import pandas as pd
from tqdm import tqdm

from labels import labels
from prompts import (
    PromptOne,
    PromptThree,
    PromptTwo,
)
from query_calls import Client, Options, Query

# Number of exemplars shown in prompt for both high and low
NUMBER_EXEMPLARS = 5


def get_arguments():
    parser = argparse.ArgumentParser(description="Arguments for the dataset")
    parser.add_argument(
        "-d", "--dataset", type=str, help="Dataset to be used from dataset/"
    )
    parser.add_argument(
        "-m", "--model", type=str, help="LLM model to be used when prompting"
    )
    return parser.parse_args()


def get_high_low(dataframe, label: str):
    out_cols = [
        "cid",
        "odorname",
        "canonicalsmiles",
        "odor_dilution",
        label,
    ]
    ordered_dataframe = dataframe.sort_values(by=label)[out_cols]
    bot_exemplars = _convert_rows_to_dict(ordered_dataframe[:NUMBER_EXEMPLARS])
    top_exemplars = _convert_rows_to_dict(ordered_dataframe[-NUMBER_EXEMPLARS:])
    return top_exemplars, bot_exemplars


def _convert_rows_to_dict(dataframe):
    return [dataframe.iloc[i].to_dict() for i in range(len(dataframe))]


def main():
    arguments = get_arguments()
    dataframe = pd.read_json(os.path.join("datasets", arguments.dataset))
    model = arguments.model
    # dataframe = pd.read_json("datasets/acid_exp.json")
    # model = "gpt-5-nano"
    # for i in tqdm(range(1), desc="Testing molecules"):
    for i in tqdm(range(len(dataframe["odorname"])), desc="Testing molecules"):
        molecule_dict = dataframe.iloc[i].to_dict()
        target_label = str(dataframe["target_label"][i])
        dataframe_filtered = dataframe.drop(i)
        top_exemplars, bot_exemplars = get_high_low(
            dataframe=dataframe_filtered, label=target_label
        )

        prompt = PromptOne(testMol=molecule_dict, targetLabel=target_label)
        print(prompt)

        # prompt = PromptTwo(
        #     testMol=molecule_dict,
        #     targetLabel=target_label,
        #     highExemplars=top_exemplars,
        #     lowExemplars=bot_exemplars,
        #     includeRatings=True,
        # )
        # print(prompt)

        # prompt = PromptThree(
        #     testMol=molecule_dict,
        #     targetLabel=target_label,
        #     highExemplars=top_exemplars,
        #     lowExemplars=bot_exemplars,
        # )
        # print(prompt)

    options = Options(
        model=model,
        max_tokens=16384,
    )
    client = Client(options)
    query = Query(
        query_type="rating",
        user_prompt=prompt,
    )
    response, tokens = client.inference(query)
    print(response)
    print(tokens)


if __name__ == "__main__":
    main()
