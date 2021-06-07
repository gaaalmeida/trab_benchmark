function GetLocalName {
  param
  (
      [Parameter(Mandatory)]
      [UInt32]$ID,

      [string]$ComputerName = $env:COMPUTERNAME
  )

  $OutputEncoding = [Console]::OutputEncoding = New-Object System.Text.Utf8Encoding

  $code = @'
[DllImport("pdh.dll", SetLastError=true, CharSet=CharSet.Unicode)]
public static extern UInt32 PdhLookupPerfNameByIndex(string szMachineName, uint dwNameIndex, System.Text.StringBuilder szNameBuffer, ref uint pcchNameBufferSize);
'@

  $buffer = New-Object System.Text.StringBuilder(1024)
  [UInt32]$bufferSize = $buffer.Capacity

  $t = Add-Type -MemberDefinition $code -PassThru -Name PerfCounter -Namespace Utility
  $rv = $t::PdhLookupPerfNameByIndex($ComputerName, $id, $buffer, [Ref]$bufferSize)

  if ($rv -eq 0)
  {
      $buffer.ToString().Substring(0, $bufferSize - 1)
  }
  else
  {
      throw 'GetLocalName : Unable to retrieve localized name. Check computer name and performance counter ID.'
  }
}

GetLocalName -ID 3518
GetLocalName -ID 3568
