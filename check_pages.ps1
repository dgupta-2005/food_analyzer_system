$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("c:\Users\dgupt\Downloads\webd\food_analyser_system\NutriVision_SRS_Specification.docx")
$pages = $doc.ComputeStatistics(2)
$doc.Close([ref]$false)
$word.Quit()
Write-Host "EXACT_WORD_PAGES:$pages"
