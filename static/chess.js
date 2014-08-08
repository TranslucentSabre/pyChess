boardSelector = "#chessBoard"

function generateBoard() {
   jQueryDiv = $(boardSelector)
   htmlString = "";
   columnArray = ["a", "b", "c", "d", "e", "f", "g", "h"];
   blackSquares = ["#a1","#c1","#e1","#g1","#b2","#d2","#f2","#h2","#a3","#c3","#e3","#g3","#b4","#d4","#f4","#h4",
                   "#a5","#c5","#e5","#g5","#b6","#d6","#f6","#h6","#a7","#c7","#e7","#g7","#b8","#d8","#f8","#h8"] 
   whiteSquares = ["#b1","#d1","#f1","#h1","#a2","#c2","#e2","#g2","#b3","#d3","#f3","#h3","#a4","#c4","#e4","#g4",
                   "#b5","#d5","#f5","#h5","#a6","#c6","#e6","#g6","#b7","#d7","#f7","#h7","#a8","#c8","#e8","#g8"] 
   for ( row = 8; row >= 0; row--) {
      for ( column = -1; column <= 7; column++) {
         if (column == -1) {
            id = row;
            if (row == 0) {
               id = "";
            }
            htmlString += '<div id="'+id+'" class="square newLine numbers">'+id+'</div>';
         }
         else if (row == 0) {
            id = columnArray[column];
            htmlString += '<div id="'+id+'" class="square horizontal letters">'+id+'</div>';
         }
         else {
            id = columnArray[column] + row;
            htmlString += '<div id="'+id+'" class="square chessSquare horizontal"></div>';
         }
      }
   }
   jQueryDiv.html(htmlString);
   $(whiteSquares.join(",")).addClass("whiteSquare");
   $(blackSquares.join(",")).addClass("blackSquare");
   $('.chessSquare[id^="a"]').addClass("left-bordered");
   $('.chessSquare[id^="h"]').addClass("right-bordered");
   $('.chessSquare[id$="8"]').addClass("top-bordered");
   $('.chessSquare[id$="1"]').addClass("bottom-bordered");
}

function capatilize(string) {
   return string.charAt(0).toUpperCase() + string.slice(1);
}

function showTurnBoard(turnString){
   $.ajax( {
      url: "/game/move/"+turnString, 
      dataType: "json",
      success: function(data, textStatus) {
         $.each( data.board, function(key, value) {
            if (value[0] != " ") {
               $("#"+key).html('<img src="/static/'+capatilize(value[1])+' '+value[0]+'.png" >');
            }
         } );
      }
   });
}

$(document).ready(function(){
  generateBoard(); 
  showTurnBoard("0");
});
   