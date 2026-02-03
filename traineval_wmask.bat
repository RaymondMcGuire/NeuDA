@echo off
setlocal

rem TODO: Update these to your dataset and config paths.
set "case_path=F:\dataset\TetGS\example-man"
set "conf_path=.\confs\neuda_wmask.conf"
set "gpu_id=0"

set "CUDA_VISIBLE_DEVICES=%gpu_id%"

echo RECONSTRUCT CASE: %case_path%
echo CONF: %conf_path%
echo GPU_ID = %gpu_id%

echo uv run python reconstruct_mesh.py --mode train --conf %conf_path% --case %case_path%
uv run python reconstruct_mesh.py --mode train --conf %conf_path% --case %case_path%

echo uv run python extract_mesh.py --conf %conf_path% --case %case_path% --eval_metric
uv run python extract_mesh.py --conf %conf_path% --case %case_path% --eval_metric

echo NeuDA train ^& evaluation done!

endlocal


pause