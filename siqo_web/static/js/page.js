//==============================================================================
// (c) SIQO PagMan Application management function
//------------------------------------------------------------------------------

var t;               // timer handler

var ha=0;            // aktualna vyska
var v=0;             // rychlost zmeny ha
var he=0;            // zelana vyska

var BS;
var FS;

var SSO;

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
// Stage Login/Content mgmt
//------------------------------------------------------------------------------
function ShowStageLogin()
{
  // Zatlaci Stage Content do pozadia
  document.getElementById("Content").style.display = "none";

  // Vystavi Stage Login do popredia
  document.getElementById("Login").style.display = "block";
}

//------------------------------------------------------------------------------
function ShowStageContent()
{
  // Zatlaci Stage Content do pozadia
  document.getElementById("Content").style.display = "block";

  // Vystavi Stage Login do popredia
  document.getElementById("Login").style.display = "none";
}
//==============================================================================
// Stage Panel mgmt
//------------------------------------------------------------------------------
function ShowStage( key )
{
  // Zatlaci vsetky panely do pozadia
  panels = document.getElementsByName("SP");
    
  for (var i = 0; i < panels.length; i++) { 
    panels[i].style.display = "none";
  }

  // Vystavi key do popredia
  document.getElementById( "SP_" + key ).style.display = "block";
}
//==============================================================================
// Object
//------------------------------------------------------------------------------
function ObjectContentControl( name, height )
{
  // Zisti, ci SS dole alebo hore
  BS = document.getElementById( name + "_BS" );
  FS = document.getElementById( name + "_FS" );
  if ( !BS ) return;
  if ( !FS ) return;

  OS = document.getElementById( name + "_OS" );
  CS = document.getElementById( name + "_CS" );
  HS = document.getElementById( name + "_HS" );

  oh = OS.clientHeight;
  ch = CS.clientHeight;
  hh = HS.clientHeight;
  bh = BS.clientHeight;
  fh = FS.clientHeight;

  v  = 0;
  ha = 0;

  if ( fh > bh ) {
    // zobrazene je Front
    he = oh - hh - ch - 11;
    ObjectScrollDown();
    
  } else {
    // zobrazene je Back
    he = bh;
    ObjectScrollUp();
  }
}
//------------------------------------------------------------------------------
function ObjectScrollDown()
{
  // naberanie rychlosti / brzdenie
  v = v + 7 ;

  // zmena aktualnej vysky
  ha = ha + v;
  if( ha > he ) ha = he;

  BS.style.height =      ha+'px';
  FS.style.height = (he-ha)+'px';
  
  // Rozhodnutie o pokracovani
  if( ha < he ) setTimeout( "ObjectScrollDown()", 50);
}
//------------------------------------------------------------------------------
function ObjectScrollUp()
{
  // naberanie rychlosti / brzdenie
  v = v + 7;

  // zmena aktualnej vysky
  ha = ha + v;
  if( ha > he ) ha = he;
  
  FS.style.height =      ha+'px';
  BS.style.height = (he-ha)+'px';
  
  // Rozhodnutie o pokracovani
  if( ha < he ) setTimeout( "ObjectScrollUp()", 50);
}
//==============================================================================
// DBTable
//------------------------------------------------------------------------------
function DBTableChanged( name )
{
  // zistenie zmeneneho atributu
  attr = document.getElementsByName( name )[0];
  attr.style.backgroundColor = "#FFFF00";

  // zistenie pozicii hranatych zatvoriek
  leftF  = name.indexOf( "[" );
  leftL  = name.lastIndexOf( "[" );
  rightF = name.indexOf( "]" );
  rightL = name.lastIndexOf( "]" );
  
  // zistenie aktualneho objektu, riadku a stlpca
  obj = name.substr( 0, leftF );
  row = name.substr( leftF+1, rightF-leftF-1 );
  col = name.substr( leftL+1, rightL-leftL-1 );

  // prikaz na UPDATE
  line = document.getElementsByName( obj + '[' + row + '][__LINE__]' )[0]; 
  line.value = 'UPDATE';
}
//==============================================================================
// Pomocne fcie
//------------------------------------------------------------------------------
function PercToInt( per )
{
   ps = per.indexOf( "%" );
   return per.substr( 0, ps );
}
//------------------------------------------------------------------------------
function PxToInt( px )
{
   ps = px.indexOf( "p" );
   return px.substr( 0, ps );
}
//------------------------------------------------------------------------------
function Debug( str )
{
  document.getElementById("SubTitle").innerHTML = str;
}
//------------------------------------------------------------------------------
// Koniec skriptu
//==============================================================================
