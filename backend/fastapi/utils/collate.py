import torch
from torch.nn.utils.rnn import pad_sequence


def collate(batch):

    try:
        docs_rel, docs_irr, queries = zip(*batch)

        docs_rel = pad_sequence(docs_rel, batch_first=True, padding_value=0)
        docs_irr = pad_sequence(docs_irr, batch_first=True, padding_value=0)
        queries = pad_sequence(queries, batch_first=True, padding_value=0)

        docs_rel_mask = (docs_rel != 0).float()

        docs_irr_mask = (docs_irr != 0).float()

        query_mask = (queries != 0).float()

        return docs_rel, docs_irr, queries, docs_rel_mask, docs_irr_mask, query_mask
    except Exception as e:
        print(f"Error in collate function: {e}")
        print(f"Batch contents: {batch}")
        raise
