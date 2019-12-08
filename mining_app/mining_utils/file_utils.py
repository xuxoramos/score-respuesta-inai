import requests
from mining_utils.Proxy import ProxyList
from requests.exceptions import HTTPError
import s3fs
from datetime import datetime
from time import sleep
import logging
logging.getLogger().setLevel("INFO")


class FileMiner:
    def __init__(self, **kwargs):
        self.proxies = ProxyList(**kwargs)
        self.attempts = 0

    def mine(self, file: dict):

        url = file["archivo_adjunto"]
        #i, p = self.proxies.get()
        response = requests.get(url, verify=False)#, proxies=p)
        try:
            response.raise_for_status()
        except HTTPError as e:
            logging.warn(e)
            self.attempts += 1
            if self.attempts > 30:
                return -1
            sleep(5)
            return self.mine(file)

        self.attempts = 0
        return response.content

class FileUploader:
    def __init__(self, instance_number: int):
        self.bucket = "s3://inai-aixsw/"
        self.s3 = s3fs.S3FileSystem(anon=False)
        self.instance_number = instance_number

    def build_path(self, file: dict):
        folio = file["folio"]
        tipo = file["tipo"]
        path = self.bucket + tipo + "/" + str(folio)
        return path

    def upload(self, content: object, file: dict):

        path = self.build_path(file)
        i = file["index"]

        if content == -1:
            with self.s3.open(self.bucket + f"problematic/{self.instance_number}/{i}", "wb") as f:
                f.write(str(datetime.now()).encode('utf-8'))
                logging.warn("... problematic file. Registered.")
                return

        with self.s3.open(path, "wb") as f:
            f.write(content)
            logging.info("... content uploaded to s3")

        with self.s3.open(self.bucket + f"done/{self.instance_number}/{i+1}", "wb") as f:
            f.write(str(datetime.now()).encode('utf-8'))
            logging.info("... marked as done")

        return

    def check_progress(self):
        done = self.s3.ls(self.bucket + f"done/{self.instance_number}/")
        done = [int(s.split("/")[3]) for s in done]
        done.sort()

        return done[-1] if len(done) > 0 else 0
