Push-Location (Split-Path -Parent $PSScriptRoot)
npx --prefix tools tsx tools/build.ts @Args
Pop-Location
