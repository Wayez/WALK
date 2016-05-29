
var doubleEliminationData = {
    "teams" : [
      ["Team 1",  "Team 2"],
      ["Team 3",  "Team 4"],
      ["Team 5",  "Team 6"],
      ["Team 7",  "Team 8"],
      ["Team 9",  "Team 10"],
      ["Team 11", "Team 12"],
      ["Team 13", "Team 14"],
      ["Team 15", "Team 16"],
    ],
    "results" : [[    /* WINNER BRACKET */
      [[3,5], [2,4], [6,3], [2,3], [1,5], [5,3], [7,2], [1,2]], 
      [[1,2], [3,4], [5,6], [7,8]],
      [[9,1], [8,2]],
      [[1,3]]
    ], [              /* LOSER BRACKET */
      [[7,8], [1,2], [3,2], [6,9]],
      [[8,2], [1,2], [6,2], [1,3]],
      [[1,2], [3,1]],
      [[3,0], [1,9]],
      [[3,2]],
      [[4,2]]
    ], [              /* FINALS */
      [[3,8], [1,2]],
      [[2,1]] 
    ]]
}
 
$(function() {
    $('div#doubleElimination.demo').bracket({
	init: doubleEliminationData})
})

