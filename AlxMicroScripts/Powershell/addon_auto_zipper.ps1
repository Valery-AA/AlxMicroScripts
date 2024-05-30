$target_subfolder = Split-Path -Path '.\AlxQuickActions' -Leaf -Resolve

$target_zip_file = 'AlxQuickActions.zip'
if (Test-Path .\$target_zip_file)
{
    Remove-Item .\$target_zip_file
}
if ( Test-Path .\$target_subfolder)
{
    Compress-Archive -Path .\$target_subfolder -Destination .\$target_subfolder.zip
}
