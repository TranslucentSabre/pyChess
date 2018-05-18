var boardSelector = "#chessBoard";
var intervalID = 0;
var refreshTimerInMs = 5000;

function buildLeftPanel(){
   var htmlString = "";
   htmlString += '<a id="fileLink" class="newLine" onclick="toggleFileVisibility();">File Selection</a>';
   htmlString += '<div hidden="" id="fileDiv"><div class="label newLine">File Name:</div><input type="text" class="horizontal" id="fileName"></input>';
   htmlString += '<input type="button" class="newLine" id="loadButton" value="Load" onclick="loadButtonClick();"></input>';
   htmlString += '<input type="button" class="horizontal" id="saveButton" value="Save" onclick="saveButtonClick();"></input>';
   htmlString += '</div>';
   htmlString += '<br/><br/><br/><br/>'
   htmlString += '<a id="gameLink" class="newLine" onclick="toggleGameVisibility();">Game Selection</a>';
   htmlString += '<div hidden="" id="GameSelection">';
   htmlString += '<select class="newLine" id="gameSelect" ><option id="tempGameSel" value="">Please Load a Game</option></select>';
   htmlString += '<input type="button" class="newLine" id="submitGameSelection" value="Select" onclick="selectGame();"></input>';
   htmlString += '<input type="button" class="horizontal" id="newGameButton" value="New Game" onclick="startNewGame();"></input>';
   htmlString += '<input type="button" class="horizontal" id="resetButton" value="Restart Game" onclick="resetGame();"></input>';
   htmlString += '<input type="button" class="horizontal" id="resetAllButton" value="Reset All Games" onclick="resetAllGames();"></input>';
   htmlString += '</div>';
   htmlString += '<br/><br/><br/><br/>';
   htmlString += '<a id="configLink" class="newLine" onclick="toggleConfigVisibility();">Configuration</a>';
   htmlString += '<div hidden="" id="configDiv">';
   htmlString += '<select class="newLine" id="configSelect" onchange="showConfigItem()"></select>';
   htmlString += '<input type="text" class="newLine" id="configValue"></input>';
   htmlString += '<input type="button" class="newLine" id="configSave" value="Save" onclick="saveConfigItem();"></input>';
   htmlString += '</div>';
   $("#leftPanel").html(htmlString);
}

function buildRightPanel(){
   var htmlString = "";
   htmlString += '<div id="results"></div>';
   htmlString += '<a id="movesLink" class="newLine" onclick="toggleMovesVisibility();">Moves</a>';
   htmlString += '<div hidden="" id="moveDiv"><select class="newLine" id="moveSelect" onchange="moveSelectChanged()"></select>';
   htmlString += '<div class="label newLine">Algebraic Notation: </div>';
   htmlString += '<input type="text" class="horizontal" id="algebraicMove"></input>';
   htmlString += '<input type="button" class="newLine" id="submitAlgebraicMove" value="Move" onclick="submitAlgebraicMove();"></input>';
   htmlString += '</div>';
   htmlString += '<br/><br/><br/><br/><br/><br/>';
   htmlString += '<a id="promoLink" class="newLine" onclick="togglePromoVisibility();">Promotion Piece (Queen)</a>';
   htmlString += '<div hidden="" id="promoDiv"><select class="newLine" id="promoSelect" >';
   promoPieces = {"Rook" : "R", "Knight" : "N", "Bishop" : "B", "Queen" : "Q"};
   $.each(promoPieces, function(key ,value) {
      htmlString += '<option id="'+key+'Promo" value="'+value+'">'+key+'</option>';
   } );
   htmlString += '</select>';
   htmlString += '</div>';
   htmlString += '<br/><br/><br/><br/><br/><br/>';
   htmlString += '<a id="tagLink" class="newLine" onclick="toggleTagVisibility();">Tags</a>';
   htmlString += '<div hidden="" id="tagDiv"><select class="newLine" id="tagSelect" onchange="selectGameTag()"></select>';
   htmlString += '<div class="label newLine">Tag Name: </div><input type="text" class="horizontal" disabled="disabled" id="tagName"></input>';
   htmlString += '<div class="label newLine">Tag Value: </div><input type="text" class="horizontal" id="tagValue"></input>';
   htmlString += '<input type="button" class="newLine" id="createTag" value="Create" onclick="createTag();"></input>';
   htmlString += '<input type="button" class="horizontal" id="deleteTag" value="Delete" onclick="deleteTag();"></input>';
   htmlString += '<input type="button" class="horizontal" id="saveTag" value="Save" onclick="saveTag();"></input>';
   htmlString += '</div>';
   $("#rightPanel").html(htmlString);
   $("#promoSelect").val("Q");
}

function generateBoard() {
   var jQueryDiv = $(boardSelector)
   var htmlString = "";
   var columnArray = ["a", "b", "c", "d", "e", "f", "g", "h"];
   var blackSquares = ["#a1","#c1","#e1","#g1","#b2","#d2","#f2","#h2","#a3","#c3","#e3","#g3","#b4","#d4","#f4","#h4",
                   "#a5","#c5","#e5","#g5","#b6","#d6","#f6","#h6","#a7","#c7","#e7","#g7","#b8","#d8","#f8","#h8"];
   var whiteSquares = ["#b1","#d1","#f1","#h1","#a2","#c2","#e2","#g2","#b3","#d3","#f3","#h3","#a4","#c4","#e4","#g4",
                   "#b5","#d5","#f5","#h5","#a6","#c6","#e6","#g6","#b7","#d7","#f7","#h7","#a8","#c8","#e8","#g8"];
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
   //Black status bar
   htmlString += '<div class="label newLine">Status for Black Player:</div><div class="horizontal" id="blackStatus"></div>';
   htmlString += '<div class="label newLine">Captured by Black Player:</div><div class="horizontal" id="blackCaptured"></div>';
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
   Game.currentlySelectedTurn = $("#moveSelect").val();
   showTurnBoard(Game.currentlySelectedTurn);
}

function enableInput() {
   setInputDisabled(false);
}

function disableInput() {
   setInputDisabled(true);
}

function setInputDisabled(disabled) {
   $("input,select").prop("disabled", disabled);
   Game.pageDisabled = disabled;
}

function toggleFileVisibility() {
   toggleDivVisibility("#fileDiv");
}

function toggleConfigVisibility() {
   toggleDivVisibility("#configDiv");
}

function toggleGameVisibility() {
   toggleDivVisibility("#GameSelection");
}

function toggleMovesVisibility() {
   toggleDivVisibility("#moveDiv");
}

function togglePromoVisibility() {
   toggleDivVisibility("#promoDiv");

   linkText = "Promotion Piece";
    var container = $("#promoDiv");

    if (container.prop("hidden") == false) {
        $("#promoLink").html(linkText);
    }
    else {
        $("#promoLink").html(linkText+" ("+$("#promoSelect :selected").html()+")");
    }

}

function toggleTagVisibility() {
   toggleDivVisibility("#tagDiv");
}

function getPromotionPiece() {
   return $("#promoSelect").val();
}

function toggleDivVisibility(divSelector) {
    var container = $(divSelector);

    if (container.prop("hidden") == false) {
        container.prop("hidden",true);
    }
    else {
        container.prop("hidden",false);
    }
}

function displaySuccessOrError(data,successCallback,errorCallback) {
    if (data.result != "Success") {
        $("#results").html(data.error);
        if (typeof errorCallback === "function") {
           errorCallback();
        }
    }
    else {
        $("#results").html(data.result);
        if (typeof successCallback === "function") {
           successCallback();
        }
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
         var whiteCurrentTurn = false;
         var blackCurrentTurn = false;
         if (Game.lastTurnSaved == turnString) {
            if (WhiteGoesNext(turnString)) {
                whiteDraggable = piecesDraggable;
                whiteCurrentTurn = true;
            }
            else {
                blackDraggable = piecesDraggable;
                blackCurrentTurn = true;
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
         var lastTurnHovers = [];
         $.each( data.board, function(key, value) {
            //Set the hover over function if this is needed
            var setHovers = false;
            if (value[0] != " ") {
               if (value[1] === "White")
               {
                   lastTurnOption = whiteDraggable;
                   setHovers = whiteCurrentTurn;
               }
               else
               {
                   lastTurnOption = blackDraggable;
                   setHovers = blackCurrentTurn;
               }
               $("#"+key).html('<img src="/static/'+capatilize(value[1])+' '+value[0]+'.png" '+lastTurnOption+' >');
               if (setHovers) {
                  $("#"+key+">img").hover(function(){Valid.startHover(key);}, Valid.stopHover);
               }
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

function timerTick() {
   if(!Game.pageDisabled) {
      displayTurn = true;
      if (Game.currentlySelectedTurn != Game.lastTurnSaved) {
         displayTurn = false;
      }
      getGameMoves(false, displayTurn);
   }
}

function getGameMoves(callback,displayTurn) {
   if ( typeof displayTurn === "undefined" ) {
      displayTurn = true;
   }
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
         Game.lastTurnSaved = data.lastTurn;
         if (displayTurn) {
            $("#moveSelect").val(data.lastTurn);
            Game.currentlySelectedTurn = Game.lastTurnSaved;
            showTurnBoard(data.lastTurn);
         }
         else {
            $("#moveSelect").val(Game.currentlySelectedTurn);
         }
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
      url: "/load",
      dataType: "json",
      type: "PUT",
      data: data,
      success: function(data, textStatus) {
         displaySuccessOrError(data,populateGameSelection);
      }
   } );
}

function loadButtonClick() {
   loadGameFile($("#fileName").val());
}

function populateGameSelection(callback) {
   $.ajax( {
      url: "/games",
      dataType: "json",
      success: function(data, textStatus) {
         var optionsString = '';
         $.each(data.games, function(_,dict) {
            optionsString += '<option id="'+dict.url+'" value="'+dict.url+'">Date: '+dict.Date+'; White: '+dict.White+'; Black: '+dict.Black+'</option>';
         } );
         $("#gameSelect").html(optionsString);
         $("#gameSelect").val("/games/"+data.currentGameIndex);
         displaySuccessOrError(data, callback)
      }
   } );
}

function selectGame() {
   var gameUrl = $("#gameSelect").val();
   if (gameUrl != "") {
      disableInput();
      $.ajax( {
         url: gameUrl,
         dataType: "json",
         type: "PUT",
         success: function(data, textStatus) {
            enableInput();
            displaySuccessOrError(data,function(){populateGameSelection(getGameMoves);populateGameTags();});
         }
      } );
   }
}

function startNewGame() {
   $.ajax( {
      url: "/games",
      type: "POST",
      dataType: "json",
      success: function(data, textStatus) {
         displaySuccessOrError(data,function(){populateGameSelection(getGameMoves);})
      }
   } );
}

function tagCreationInProgress() {
   return $("#createTag").val() == "Cancel" ? true : false;
}

function beginTagCreation() {
   $("#tagName").prop("disabled", false);
   $("#createTag").val("Cancel");
   $("#deleteTag").prop("disabled", true);
}

function cancelTagCreation() {
   $("#tagName").prop("disabled", true);
   $("#createTag").val("Create");
   $("#deleteTag").prop("disabled", false);
}

function populateGameTags(selected) {
   var tagUrl = "/game/tag"
   $.ajax( {
      url: tagUrl,
      dataType: "json",
      success: function(data, textStatus) {
         var tagsString = '';
         $.each(data.tags, function(_,dict) {
            $.each(dict, function(key, value) {
               if (selected == null) {
                  selected = key
               }
               tagsString += '<option id="tag_'+key+'" value="'+key+'">'+key+'</option>';
            } );
         } );
         $("#tagSelect").html(tagsString);
         $("#tagSelect").val(selected);
         selectGameTag();
      }
   } );
}

function createTag() {
   if(tagCreationInProgress()) {
      cancelTagCreation();
      $("#tagSelect").val(Game.previouslySelectedTagValue);
      selectGameTag();
   }
   else {
      beginTagCreation();
      $("#tagName").val("");
      $("#tagValue").val("");
   }
}

function selectGameTag() {
   cancelTagCreation();
   var tagUrl = "/game/tag/"+$("#tagSelect").val();
   $.ajax( {
      url: tagUrl,
      dataType: "json",
      success: function(data, textStatus) {
         name = $("#tagSelect").val();
         $("#tagName").val(name);
         $("#tagValue").val(data.tag[name]);
         Game.previouslySelectedTagValue = name;
      }
   } );
}

function saveTag() {
   cancelTagCreation();
   var tagUrl = "/game/tag";
   var tagNameVal = $("#tagName").val();
   if(tagNameVal === "") {
      $("#results").html("No Tag Name Specified");
      //Note this is really "cancelCreateTag" due to our current state
      createTag();
      return;
   }
   $.ajax( {
      url: tagUrl,
      type: "POST",
      dataType: "json",
      data : { tagName  : tagNameVal,
               tagValue : $("#tagValue").val() },
      success : function(data, textStatus) {
         populateGameTags(tagNameVal);
      }
   } );
}

function deleteTag() {
   var tagUrl = "/game/tag/"+$("#tagSelect").val();
   var selectedTag = $("#tagSelect").val();
   //Here I cheat and know that the top seven will only be defaulted becuase they are the Seven Tag Roster
   //Revert to the first entry once we delete a non-STR tag
   if($("#tagSelect")[0].selectedIndex >= 7) {
      selectedTag = $("#tagSelect > option:first").val();
   }
   $.ajax( {
      url: tagUrl,
      type: "DELETE",
      dataType: "json",
      success: function(data, textStatus) {
         populateGameTags(selectedTag);
      }
   } );
}

function saveGameFile(file) {
   if (file !== "") {
      var data = { fileName : file };
   }
   else {
      data = {}
   }
   $.ajax( {
      url: "/save",
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
}

function resetGame() {
   $.ajax( {
      url: "/game",
      dataType: "json",
      type: "DELETE",
      data: {},
      success: function(data, textStatus) {
         displaySuccessOrError(data,function(){populateGameSelection(getGameMoves);})
      }
   } );
}

function resetAllGames() {
   $.ajax( {
      url: "/games",
      dataType: "json",
      type: "DELETE",
      data: {},
      success: function(data, textStatus) {
         displaySuccessOrError(data,function(){populateGameSelection(getGameMoves);})
      }
   } );
}

var Config = {
   values : {},
   backToFront : {"import"    : "Default File To Load",
                  "export"    : "Default File To Save",
                  "strict"    : "Strict Algebraic Move Parsing",
                  "random"    : "Random pieces on new game",
                  "threshold" : "Maximum difference between piece values in random games"},
   frontToBack : {"Default File To Load" : "import",
                  "Default File To Save" : "export",
                  "Strict Algebraic Move Parsing" : "strict",
                  "Random pieces on new game" : "random",
                  "Maximum difference between piece values in random games" : "threshold"},
};

function showConfigItem() {
   backendConfig = Config.frontToBack[$("#configSelect").val()];
   $("#configValue").val(Config.values[backendConfig]);
}

function getConfiguration() {
   $.ajax( {
      url: "/config",
      dataType: "json",
      success: function(data, textStatus) {
         var optionsString = '';
         Config.values = data.config;
         previousVal = $("#configSelect").val();
         $.each(Config.values, function(name,_) {
            if(Config.backToFront[name])
            {
               name = Config.backToFront[name];
               if (previousVal == null) {
                  previousVal = name;
               }
               optionsString += '<option id="config'+name+'" value="'+name+'">'+name+'</option>';
            }
         } );
         $("#configSelect").html(optionsString);
         $("#configSelect").val(previousVal);
         showConfigItem();
      }
   } );
}

function saveConfigItem() {
   backendConfig = Config.frontToBack[$("#configSelect").val()];
   data = { value : $("#configValue").val() };
   $.ajax( {
      url: "/config/"+backendConfig,
      dataType: "json",
      type: "PUT",
      data: data,
      success: function(data, textStatus) {
         displaySuccessOrError(data, getConfiguration());
      }
   } );
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

function submitCoordinateMove(firstCoord, secondCoord, promotion) {
    if (typeof promotion === 'undefined' || promotion === null) {
        promotion = "";
    }
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
        if (move.promotion !== "") {
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
   lastTurnSaved : "0",
   currentlySelectedTurn : "0",
   previouslySelectedTagValue : "",
   pageDisabled : false
};

var Valid = {
   stillHovering : false,
   currentCoord : "",
   highlightedSquares : [],
   
   startHover : function(coord) {
      Valid.stillHovering = true;
      Valid.currentCoord = coord;
      window.setTimeout(Valid.fireHover, 1000);
   },

   stopHover : function() {
      Valid.stillHovering = false;
      Valid.currentCoord = "";
      Valid.clearHighlight();
   },

   fireHover: function() {
      if(Valid.stillHovering) {
         $.ajax( {
            url: "/game/moves/"+Valid.currentCoord,
            dataType: "json",
            success: function(data, textStatus) {
               //Remove piece name from dataset
               squares = data.moves
               squares.splice(0, 1);
               $.each(squares, function(_, dict) {
                  $.each(dict, function(key, _) {
                     Valid.highlightedSquares.push(key);
                     $("#"+key).addClass("greenSquare");
                  })
               })
            }
         });
      }
   },

   clearHighlight : function() {
      $.each(Valid.highlightedSquares, function(_, id) {
         $("#"+id).removeClass("greenSquare")
      })
      Valid.highlightSquares = [];
   }
}

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
         promotionPiece = null;

         sourceID = Drag.jQuerySource.attr("id");
         destID = Drag.jQueryDest.attr("id");
         transferData = evt.originalEvent.dataTransfer.getData("text/html");
         pieceInformation = transferData.match(/[A-Z][a-z]+ [PRKNBQ].png/)[0].split(" ");
         if (pieceInformation[1][0] === "P") {
            if ( (pieceInformation[0] === "White" && destID[1] === "8") || 
                 (pieceInformation[0] === "Black" && destID[1] === "1") ) {
               promotionPiece = getPromotionPiece();
            }
         }
         Drag.jQueryDest.html(transferData);
         submitCoordinateMove(sourceID, destID, promotionPiece);
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
   populateGameSelection();
   getGameMoves();
   populateGameTags();
   getConfiguration();
   intervalID = window.setInterval(timerTick, refreshTimerInMs);
});
