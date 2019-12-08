from mining_utils.Proxy import ProxyList
from mining_utils.file_utils import FileMiner, FileUploader
import pandas as pd
import logging
logging.getLogger().setLevel("INFO")
from sys import argv

if __name__ == "__main__":
    
    batch_id = argv[1]
    batch_id = int(batch_id)
    logging.info(f"BATCH: {batch_id}")
    miner = FileMiner()
    uploader = FileUploader(batch_id)
    data = pd.read_csv(f"data/adjuntos/batch-{batch_id}.csv").reset_index(drop=False)
    max_done = uploader.check_progress()
    for i, r in data.iterrows():

        filedict = r.to_dict()
        j = filedict["index"]

        logging.info(f"Now in file number {j}")

        if j <= max_done:
            logging.info("...been here before")
            continue

        content = miner.mine(filedict)
        uploader.upload(content, filedict)

