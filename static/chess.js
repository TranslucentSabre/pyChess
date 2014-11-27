var boardSelector = "#chessBoard";

function buildLeftPanel(){
   var htmlString = "";
   htmlString += '<div id="SaveLoad"><div class="label newLine">File Name:</div><input type="text" class="horizontal" id="fileName"></input>';
   htmlString += '<input type="button" class="newLine" id="loadButton" value="Load" onclick="loadButtonClick();"></input>';
   htmlString += '<input type="button" class="horizontal" id="saveButton" value="Save" onclick="saveButtonClick();"></input>';
   htmlString += '</div>';
   $("#leftPanel").html(htmlString);
}

function buildRightPanel(){
   var htmlString = "";
   htmlString += '<div id="results"></div>';
   htmlString += '<select class="newLine" id="moveSelect" onchange="moveSelectChanged()"></select>';
   htmlString += '<div class="label newLine">Algebraic Notation: </div>';
   htmlString += '<input type="text" class="horizontal" id="algebraicMove"></input>';
   htmlString += '<input type="button" class="newLine" id="submitAlgebraicMove" value="Move" onclick="submitAlgebraicMove();"></input>';
   $("#rightPanel").html(htmlString);
}

function generateBoard() {
   var jQueryDiv = $(boardSelector)
   var htmlString = "";
   var columnArray = ["a", "b", "c", "d", "e", "f", "g", "h"];
   var blackSquares = ["#a1","#c1","#e1","#g1","#b2","#d2","#f2","#h2","#a3","#c3","#e3","#g3","#b4","#d4","#f4","#h4",
                   "#a5","#c5","#e5","#g5","#b6","#d6","#f6","#h6","#a7","#c7","#e7","#g7","#b8","#d8","#f8","#h8"];
   var whiteSquares = ["#b1","#d1","#f1","#h1","#a2","#c2","#e2","#g2","#b3","#d3","#f3","#h3","#a4","#c4","#e4","#g4",
                   "#b5","#d5","#f5","#h5","#a6","#c6","#e6","#g6","#b7","#d7","#f7","#h7","#a8","#c8","#e8","#g8"];
   //Black status bar
   htmlString += '<div class="label newLine">Status for Black Player:</div><div class="horizontal" id="blackStatus"></div>';
   htmlString += '<div class="label newLine">Captured by Black Player:</div><div class="horizontal" id="blackCaptured"></div>';
   for ( var row = 8; row >= 0; row--) {
      for ( var column = -1; column <= 7; column++) {
         if (column == -1) {
            var id = row;
            if (row === 0) {
               id = "";
            }
            htmlString += '<div id="'+id+'" class="square newLine numbers">'+id+'</div>';
         }
         else if (row === 0) {
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

function displaySuccessOrError(data) {
    if (data.result != "Success") {
        $("#results").html(data.error);
    }
    else {
        $("#results").html(data.result);
    }
}

function enableDragFunctionality() {
   $(boardSelector).on("dragstart", ".chessSquare img", Drag.dragStart);
   $(boardSelector).on("drop", ".chessSquare", Drag.dragDrop);
   $(boardSelector).on("dragover", ".chessSquare", Drag.dragOver);
}

function disableDragFunctionality() {
   $(boardSelector).off("dragstart", ".chessSquare img", Drag.dragStart);
   $(boardSelector).off("drop", ".chessSquare", Drag.dragDrop);
   $(boardSelector).off("dragover", ".chessSquare", Drag.dragOver);
}

function WhiteGoesNext(turnString) {
    if (turnString === "0" || turnString.indexOf("...") > 0) {
        return true;
    }
    else {
        return false;
    }
}

function showTurnBoard(turnString) {
   $.ajax( {
      url: "/game/move/"+turnString,
      dataType: "json",
      success: function(data, textStatus) {
         $(".chessSquare").html("");
         var piecesDraggable = 'draggable="true"';
         var piecesNotDraggable = 'draggable="false"';
         var whiteDraggable = piecesNotDraggable;
         var blackDraggable = piecesNotDraggable;
         if (Game.lastTurnSaved == turnString) {
            if (WhiteGoesNext(turnString)) {
                whiteDraggable = piecesDraggable;
            }
            else {
                blackDraggable = piecesDraggable;
            }
            enableDragFunctionality();
            $("#algebraicMove").attr("disabled",false);
            $("#submitAlgebraicMove").attr("disabled", false);
         }
         else {
            disableDragFunctionality();
            $("#algebraicMove").attr("disabled",true);
            $("#submitAlgebraicMove").attr("disabled",true);
         }
         var lastTurnOption = "";
         $.each( data.board, function(key, value) {
            if (value[0] != " ") {
               if (value[1] === "white")
               {
                   lastTurnOption = whiteDraggable;
               }
               else
               {
                   lastTurnOption = blackDraggable;
               }
               $("#"+key).html('<img src="/static/'+capatilize(value[1])+' '+value[0]+'.png" '+lastTurnOption+' >');
            }
         } );
         //Black metadata
         var htmlString = "";
         $.each( data.blackCaptured, function(_, value) {
            htmlString += '<img class="horizontal" src="/static/White '+value+'.png" >';
         } );
         $("#blackCaptured").html(htmlString);
         var jQueryStatus = $("#blackStatus");
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

function getGameMoves(callback) {
   $.ajax( {
      url: "/game/move",
      dataType: "json",
      success: function(data, textStatus) {
         displaySuccessOrError(data);
         var optionsString = '';
         $.each(data.turns, function(_,dict) {
            $.each(dict, function(key, value) {
               optionsString += '<option id="'+key+'" value="'+key+'">'+key+': '+value+'</option>';
            } );
         } );
         $("#moveSelect").html(optionsString);
         $("#moveSelect").val(data.lastTurn);
         Game.lastTurnSaved = data.lastTurn;
         showTurnBoard(data.lastTurn);
         if (typeof callback === "function") {
             callback();
         }
      }
   } );
}

function loadGameFile(file) {
   if (file !== "") {
      var data = { fileName : file };
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
         displaySuccessOrError(data);
      }
   } );
}

function loadButtonClick() {
   loadGameFile($("#fileName").val());
   getGameMoves();
}

function saveGameFile(file) {
   if (file !== "") {
      var data = { fileName : file };
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
         displaySuccessOrError(data);
      }
   } );
}

function saveButtonClick() {
   saveGameFile($("#fileName").val());
   getGameMoves();
}

var Move = {
  ALGEBRAIC : "algebra",
  COORDINATE : "coordinate",

  method : "",
  algebraString : "",
  firstCoord : "",
  secondCoord : "",
  promotion : "",

  clear : function() {
      Move.method = "";
      Move.algebraString = "";
      Move.firstCoord = "";
      Move.secondCoord = "";
      Move.promotion = "";
  }
};

function submitCoordinateMove(firstCoord, secondCoord, promotion="") {
    Move.clear();
    Move.method = Move.COORDINATE;
    Move.firstCoord = firstCoord;
    Move.secondCoord = secondCoord;
    Move.promotion = promotion;
    makeMove(Move);
}

function submitAlgebraicMove() {
    Move.clear();
    Move.method = Move.ALGEBRAIC;
    Move.algebraString = $("#algebraicMove").val();
    makeMove(Move);
}

function makeMove(move) {
    var data = { method : move.method };
    if (move.method === Move.ALGEBRAIC) {
        data.algebra = move.algebraString;
    }
    else if (move.method === Move.COORDINATE) {
        data.firstCoord = move.firstCoord;
        data.secondCoord = move.secondCoord;
        if (move.promotion != "") {
            data.promotion = move.promotion;
        }
    }
    var printReturnAndGetMoves = function(data, textStatus) {
        getGameMoves(function(){displaySuccessOrError(data)});
    }
    $.ajax( {
        url: "/game/move",
        dataType: "json",
        type: "POST",
        data: data,
        success: function(data, textStatus) {
            if (data.result != "Success") {
                printReturnAndGetMoves(data);
            }
            else {
                $.ajax( {
                    url: data.url,
                    dataType: "json",
                    type: "PUT",
                    data: {},
                    success: printReturnAndGetMoves
                });
            }
        }
    });
}



var Game = {
   lastTurnSaved : "0"
};

var Drag = {
   jQuerySource : null,
   jQueryDest : null,

   //This is run on the img itself, hence the getting of the parent
   dragStart : function(evt) {
      Drag.jQuerySource = $(evt.target).parent();
      var transferHTML = Drag.jQuerySource.html();
      evt.originalEvent.dataTransfer.effectAllowed = "move";
      evt.originalEvent.dataTransfer.setData('text/html', transferHTML);
   },

   //These are run on the divs
   dragDrop : function(evt) {
      if (evt.stopPropagation) {
         evt.stopPropagation();
      }
      Drag.dragOver(evt); //Stop the propogation of the event

      Drag.jQueryDest = $(evt.currentTarget);
      if (Drag.jQuerySource[0] !== Drag.jQueryDest[0]) {

         Drag.jQuerySource.html("");
         Drag.jQueryDest.html(evt.originalEvent.dataTransfer.getData("text/html"));
      }
      Drag.jQuerySource = null;
      Drag.jQueryDest = null;
   },

   dragOver : function(evt) {
      if (evt.preventDefault) {
         evt.preventDefault(); // Necessary. Allows us to drop.
      }
   }
};


$(document).ready(function() {
   buildStartingHtml();
   getGameMoves();
});
