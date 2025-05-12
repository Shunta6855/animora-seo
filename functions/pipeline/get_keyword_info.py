# ---------------------------------------------------------------------------------  # 
#                   キーワードに関する過去の指標データを取得する実行コード                    #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os
import sys
from dotenv import load_dotenv, find_dotenv

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from src.utils.google_ads import generate_historical_metrics

_ = load_dotenv(find_dotenv())

# ----------------------------------
# 過去指標データを取得する関数
# ----------------------------------
def main(client, customer_id):
    """
    The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
    """
    generate_historical_metrics(client, customer_id)

if __name__ == "__main__":
    customer_id = os.getenv("GOOGLE_ADS_CUSTOMER_ID")
    if not customer_id:
        raise ValueError("GOOGLE_ADS_CUSTOMER_ID is not set in the .env file.")

    # GoogleAdsClient will read the google-ads.yaml configuration file in the home directory.
    googleads_client = GoogleAdsClient.load_from_storage(
        "/home/azureuser/animalia-seo/google-ads.yaml",
        version="v19"
    )

    try:
        main(googleads_client, customer_id)
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name} and includes the following errors:\n"
        )
        for error in ex.failure.errors:
            print(f"Error with message '{error.message}'")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)