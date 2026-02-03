@echo off
setlocal

set "case=%~1"
set "conf=%~2"
set "gpu_id=%~3"

set "CUDA_VISIBLE_DEVICES=%gpu_id%"

echo RECONSTRUCT CASE: %case%
echo CONF: %conf%
echo GPU_ID = %gpu_id%

echo uv run python reconstruct_mesh.py --mode train --conf %conf% --case %case%
uv run python reconstruct_mesh.py --mode train --conf %conf% --case %case%

echo uv run python extract_mesh.py --conf %conf% --case %case% --eval_metric
uv run python extract_mesh.py --conf %conf% --case %case% --eval_metric

echo NeuDA train ^& evaluation done!

endlocal
