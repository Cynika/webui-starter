VRAM_ranges = {"2G显存": [0, 3], "4G显存": [3, 5], "6G显存": [5, 7], "8G显存及以上": [7, 99]}

VRAM_args = {"无有效显存": "", "2G显存": "--lowvram", "4G显存": "--medvram", "6G显存": "--medvram", "8G显存及以上": ""}
cmpt_args = {"正常模式(无需兼容)": "", "16xx显卡兼容模式": "--precision full --no-half"}
GPU_args = {"0": "--skip-torch-cuda-test --precision full --no-half --use-cpu all", "1": ""}
component_args = {"xformers优化": "--xformers", "share公开": "--share", "api接口": "--api",
                  "OutPaint(√api)": "--cors-allow-origins=https://www.painthua.com --api",
                  "deepdanbooru": "--deepdanbooru", "UI夜间模式": "--theme=dark"}

update_file = "./update_webui更新.bat"
bat_file = "./start_webui启动.bat"
arg_line = "set COMMANDLINE_ARGS="

model_dir = "./models/Stable-diffusion"
emb_dir = "./embeddings"
hypernetworks_dir = "./models/hypernetworks"
extensions_dir = "./extensions"
