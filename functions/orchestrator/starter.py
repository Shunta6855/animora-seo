# ---------------------------------------------------------------------------------  # 
#                         Orchestrator を開始する HTTPトリガー                     　   #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import azure.durable_functions as df
import azure.functions as func
from function_app import app

@app.function_name(name="run_pipeline") # 関数名を Azure Functions に合わせる
@app.route(route="runPipeline", methods=["GET", "POST"]) # HTTP トリガー
@app.durable_client_input(client_name="client") # Durable Client のバインド
async def run_pipeline(
    req: func.HttpRequest, 
    client: df.DurableOrchestrationClient
) -> func.HttpResponse:
    # JSON ボディからキーワードと slug取得
    try:
        body = req.get_json()
        keyword = body.get("keyword")
        slug = body.get("slug")
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    if not keyword:
        return func.HttpResponse("keyword missing", status_code=400)
    if not slug:
        return func.HttpResponse("slug missing", status_code=400)
    
    # ここで await して文字列の ID を取得
    instance_id = await client.start_new("orchestrator", None, {
        "keyword": keyword,
        "slug": slug,
    })
    return client.create_check_status_response(req, instance_id)

__all__ = ["app"]