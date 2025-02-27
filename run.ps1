# Save the current location and switch to this script's directory.
# Note: This shouldn't fail; if it did, it would indicate a
#       serious system-wide problem.
$prevPwd = $PWD; Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot

try {
 py -m src
}
finally {
  # Restore the previous location.
  $prevPwd | Set-Location
}
