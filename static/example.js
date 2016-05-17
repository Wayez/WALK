/*(var doubleElimination = {
    "teams": [
	["Team 1", "Team 2"],
	["Team 3", "Team 4"]
    ],
    "results": [            // List of brackets (three since this is double elimination)
	[                     // Winner bracket
	    [[1, 2], [3, 4]],   // First round and results
	    [[5, 6]]            // Second round
	],
	[                     // Loser bracket
	    [[7, 8]],           // First round
	    [[9, 10]]           // Second round
	],
	[                     // Final "bracket"
	    [                   // First round
		[11, 12],         // Match to determine 1st and 2nd
		[13, 14]          // Match to determine 3rd and 4th
	    ],
	    [                   // Second round
		[15, 16]          // LB winner won first round (11-12) so need a final decisive round
	    ]
	]
    ]
};*/

var doubleEliminationData = {
    teams : [
      ["Team 1", "Team 2"],
      ["Team 3", "Team 4"]
    ],
    results : [[      /* WINNER BRACKET */
      [[1,2], [3,4]], /* first and second matches of the first round */
      [[5,6]]         /* second round */
    ], [              /* LOSER BRACKET */
      [[7,8]],        /* first round */
      [[9,10]]        /* second round */
    ], [              /* FINALS */
      [[1,12], [13,14]],
      [[15,16]]       /* LB winner won first round so need a rematch */
    ]]
};
 
$(function() {
    $('div#doubleElimination. demo').bracket({
      init: doubleEliminationData})
});
