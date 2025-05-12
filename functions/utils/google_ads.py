# ---------------------------------------------------------------------------------  # 
#                    キーワードに関する過去の指標データを取得する関数定義                     #
# ---------------------------------------------------------------------------------  #

# ----------------------------------
# 過去指標データを取得する関数
# ----------------------------------
def generate_historical_metrics(client, customer_id):
    """
    Generates historical metrics and saves them to PostgreSQL Database

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
    """
    googleads_service = client.get_service("GoogleAdsService")
    keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordHistoricalMetricsRequest")
    request.customer_id = customer_id
    request.keywords = ["ペットSNS", "ペットアプリ", "ペット", "犬", "猫"]
    # Geo target constant 2392 is for Japan
    request.geo_target_constants.append(googleads_service.geo_target_constant_path("2392"))
    request.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        # Limit the search to Google Search
    request.language = googleads_service.language_constant_path("1005")
    response = keyword_plan_idea_service.generate_keyword_historical_metrics(request)

    for result in response.results:
        metrics = result.keyword_metrics
        print(
            f"The search query '{result.text}' (and the following variants: "
            f"'{result.close_variants if result.close_variants else 'None'}'), "
            "generated the following historical metrics:\n"
        )

        # Approximate number of monthly searches on this query averaged for the past 12 months
        print(f"\tApproximate monthly searches: {metrics.avg_monthly_searches}")

        # The competition level for this search query
        print(f"\tCompetition level: {metrics.competition}")

        # The competition index for this search query in the range [0, 100]
        # This shows how competitive ad placement is for a keyword
        print(f"\tCompetition index: {metrics.competition_index}")

        # Top of the page bid low range (20th percentile) in micros for the keyword
        print(f"\tTop of the page bid low range: {metrics.low_top_of_page_bid_micros}")

        # Top of the page bid high range (80th percentile) in micros for the keyword
        print(f"\tTop of the page bid high range: {metrics.high_top_of_page_bid_micros}")

        # Approximate number of searches on this query for the past 12 months
        for month in metrics.monthly_search_volumes:
            print(
                f"\tApproximately {month.monthly_searches} searches in "
                f"{month.month.name}, {month.month.year}"
            )

        



