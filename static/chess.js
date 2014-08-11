boardSelector = "#chessBoard"

function buildLeftPanel(){
   htmlString = "";
   htmlString += '<div id="SaveLoad"><div class="label newLine">File Name:</div><input type="text" class="horizontal" id="fileName"></input>';
   htmlString += '<input type="button" class="newLine" id="loadButton" value="Load" onclick="loadButtonClick();"></input>';
   htmlString += '<input type="button" class="horizontal" id="saveButton" value="Save" onclick="saveButtonClick();"></input>';
   htmlString += '</div>';
   $("#leftPanel").html(htmlString);
}

function buildRightPanel(){
   htmlString = "";
   htmlString += '<div id="results"></div>';
   htmlString += '<select id="moveSelect" onchange="moveSelectChanged()"></select>';
   $("#rightPanel").html(htmlString);
}

function generateBoard() {
   jQueryDiv = $(boardSelector)
   htmlString = "";
   columnArray = ["a", "b", "c", "d", "e", "f", "g", "h"];
   blackSquares = ["#a1","#c1","#e1","#g1","#b2","#d2","#f2","#h2","#a3","#c3","#e3","#g3","#b4","#d4","#f4","#h4",
                   "#a5","#c5","#e5","#g5","#b6","#d6","#f6","#h6","#a7","#c7","#e7","#g7","#b8","#d8","#f8","#h8"];
   whiteSquares = ["#b1","#d1","#f1","#h1","#a2","#c2","#e2","#g2","#b3","#d3","#f3","#h3","#a4","#c4","#e4","#g4",
                   "#b5","#d5","#f5","#h5","#a6","#c6","#e6","#g6","#b7","#d7","#f7","#h7","#a8","#c8","#e8","#g8"];
   //Black status bar
   htmlString += '<div class="label newLine">Status for Black Player:</div><div class="horizontal" id="blackStatus"></div>';
   htmlString += '<div class="label newLine">Captured by Black Player:</div><div class="horizontal" id="blackCaptured"></div>';
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
   //White status bar
   htmlString += '<div class="label newLine">Status for White Player:</div><div class="horizontal" id="whiteStatus"></div>';
   htmlString += '<div class="label newLine">Captured by White Player:</div><div class="horizontal" id="whiteCaptured"></div>';
   jQueryDiv.html(htmlString);
   $(whiteSquares.join(",")).addClass("whiteSquare");
   $(blackSquares.join(",")).addClass("blackSquare");
   $('.chessSquare[id^="a"]').addClass("left-bordered");
   $('.chessSquare[id^="h"]').addClass("right-bordered");
   $('.chessSquare[id$="8"]').addClass("top-bordered");
   $('.chessSquare[id$="1"]').addClass("bottom-bordered");
}

function buildStartingHtml() {
   buildLeftPanel();
   generateBoard();
   buildRightPanel();
}

function capatilize(string) {
   return string.charAt(0).toUpperCase() + string.slice(1);
}

function moveSelectChanged() {
   showTurnBoard($("#moveSelect").val());
}

function showTurnBoard(turnString) {
   $.ajax( {
      url: "/game/move/"+turnString, 
      dataType: "json",
      success: function(data, textStatus) {
         $(".chessSquare").html("");
         $.each( data.board, function(key, value) {
            if (value[0] != " ") {
               $("#"+key).html('<img src="/static/'+capatilize(value[1])+' '+value[0]+'.png" >');
            }
         } );
         //Black metadata
         htmlString = "";
         $.each( data.blackCaptured, function(_, value) {
            htmlString += '<img class="horizontal" src="/static/White '+value+'.png" >';
         } );
         $("#blackCaptured").html(htmlString);
         jQueryStatus = $("#blackStatus");
         jQueryStatus.html("Normal").css("color","black");
         if (data.blackStatus.checked && !data.blackStatus.mated) {
            jQueryStatus.html("Checked").css("color","green");
         }
         else if (data.blackStatus.mated) {
            jQueryStatus.html("Check Mate").css("color", "red");
         }
         //White metadata
         htmlString = "";
         $.each( data.whiteCaptured, function(_, value) {
            htmlString += '<img class="horizontal" src="/static/Black '+value+'.png" >';
         } );
         $("#whiteCaptured").html(htmlString);
         jQueryStatus = $("#whiteStatus");
         jQueryStatus.html("Normal").css("color","black");
         if (data.whiteStatus.checked && !data.whiteStatus.mated) {
            jQueryStatus.html("Checked").css("color","green");
         }
         else if (data.whiteStatus.mated) {
            jQueryStatus.html("Check Mate").css("color", "red");
         }
      }
   });
}

function loadGameFile(file) {
   if (file != "") {
      data = { fileName : file };
   }
   else {
      data = {}
   }
   $.ajax( {
      url: "/game/load",
      dataType: "json",
      type: "PUT",
      data: data,
      success: function(data, textStatus) {
         $("#results").html(data.result);
      }
   } );
}

function loadButtonClick() {
   loadGameFile($("#fileName").val());
   getGameMoves();
}

function saveGameFile(file) {
   if (file != "") {
      data = { fileName : file };
   }
   else {
      data = {}
   }
   $.ajax( {
      url: "/game/save",
      dataType: "json",
      type: "PUT",
      data: data,
      success: function(data, textStatus) {
         $("#results").html(data.result);
      }
   } );
}

function saveButtonClick() {
   saveGameFile($("#fileName").val());
   getGameMoves();
}


function getGameMoves() {
   $.ajax( {
      url: "/game/move",
      dataType: "json",
      success: function(data, textStatus) {
         $("#results").html(data.result);
         optionsString = '';
         $.each(data.turns, function(key, value) {
            optionsString += '<option id="'+key+'" value="'+key+'">'+key+': '+value+'</option>';
         } );
         $("#moveSelect").html(optionsString);
         $("#moveSelect").val(data.lastTurn);
         showTurnBoard(data.lastTurn);
      }
   } );
}


$(document).ready(function() {
   buildStartingHtml();
   getGameMoves();
});
   
