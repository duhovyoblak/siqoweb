//==============================================================================
// (c) SIQO PagMan Application management function
//------------------------------------------------------------------------------

initId = "x";

//==============================================================================
// Bar menu mgmt
//------------------------------------------------------------------------------
function BarMenuWinHide()
{
  // Zatlaci vsetky okna BarMenu
  wins = document.getElementsByName("BarMenuItemWindow");
    
  for (var i = 0; i < wins.length; i++) { 
    wins[i].style.display="none";
  }
}
//------------------------------------------------------------------------------
function BarMenuWinShow( id )
{
  BarMenuWinHide();
  
  win = document.getElementById( id + "_window" );
  win.style.display="block";  
}
//==============================================================================
// Flash/Login/Content mgmt
//------------------------------------------------------------------------------
function HideBase()
{
  // Zatlaci vsetky elementy do pozadia
  document.getElementById("Flash"  ).style.display = "none";
  document.getElementById("Content").style.display = "none";
}
//------------------------------------------------------------------------------
function ShowElement(id)
{
  // Zatlaci base elementy pozadia
  HideBase();

  // Vystavi element ID do popredia
  document.getElementById(id).style.display = "block";
}
//------------------------------------------------------------------------------
function InitElement(id)
{
  // Flash ma prioritu 1, uz nemozno nastavit na vyssiu prioritu
  if (initId=='Flash') return;
        
  // Priorita elem je >= ako existujuce nastavenie, nastavim na elem
  initId = id;
}
//------------------------------------------------------------------------------
function ShowInitElement()
{
  ShowElement(initId);
}
//------------------------------------------------------------------------------
function Debug( str )
{
  s = document.getElementById("HeaderComment").innerHTML = str;
  document.getElementById("HeaderComment").innerHTML = s + "," + str;
}
//------------------------------------------------------------------------------
// Koniec skriptu
//==============================================================================
