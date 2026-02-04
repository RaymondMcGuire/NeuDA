@echo off
setlocal

rem TODO: Update these paths to your dataset.
set "case_path=D:\GS-project\PaddleSeg\output"

rem Optional: override these if your structure is different.
rem set "image_dir=D:\GS-project\PaddleSeg\output\images"
rem set "sparse_dir=D:\GS-project\PaddleSeg\output\sparse\0"
rem set "mask_dir=D:\GS-project\PaddleSeg\output\mask"

rem Actions
set "do_delete=--delete"
set "delete_masks=--delete-masks"
set "dry_run="
set "mask_arg="
set "rename_after=1"
set "rename_digits=4"
set "rename_out_dir="
set "rename_masks=1"

if defined mask_dir (
  set "mask_arg=--mask-dir %mask_dir%"
)

echo Checking unregistered images...
if defined image_dir (
  if defined sparse_dir (
    uv run python tools\list_unregistered_images.py "%case_path%" --image-dir "%image_dir%" --sparse-dir "%sparse_dir%" ^
      %do_delete% %delete_masks% %dry_run% %mask_arg%
  ) else (
    uv run python tools\list_unregistered_images.py "%case_path%" --image-dir "%image_dir%" ^
      %do_delete% %delete_masks% %dry_run% %mask_arg%
  )
) else (
  if defined sparse_dir (
    uv run python tools\list_unregistered_images.py "%case_path%" --sparse-dir "%sparse_dir%" ^
      %do_delete% %delete_masks% %dry_run% %mask_arg%
  ) else (
    uv run python tools\list_unregistered_images.py "%case_path%" ^
      %do_delete% %delete_masks% %dry_run% %mask_arg%
  )
)

if "%rename_after%"=="1" (
  if defined rename_out_dir (
    set "rename_out_dir_arg=--out-dir %rename_out_dir%"
  ) else (
    set "rename_out_dir_arg="
  )
  if defined image_dir (
    set "rename_image_dir=%image_dir%"
  ) else (
    if exist "%case_path%\images" (
      set "rename_image_dir=%case_path%\images"
    ) else (
      set "rename_image_dir=%case_path%\image"
    )
  )
  echo Renaming images in "%rename_image_dir%"...
  uv run python tools\rename_images.py "%rename_image_dir%" --digits %rename_digits% %rename_out_dir_arg%
  if "%rename_masks%"=="1" (
    if defined mask_dir (
      set "rename_mask_dir=%mask_dir%"
    ) else (
      set "rename_mask_dir=%case_path%\mask"
    )
    if exist "%rename_mask_dir%" (
      echo Renaming masks in "%rename_mask_dir%"...
      uv run python tools\rename_images.py "%rename_mask_dir%" --digits %rename_digits% %rename_out_dir_arg%
    )
  )
)

endlocal

pause
