<html>
    <head>
      <script type="text/javascript">
	var i = 2;
	function addFields(){
	    var newdiv = document.createElement("div");
	    newdiv.innerHTML = "<input type='text' name='name"+i+"' placeholder='Team "+i+"'><br>";
	    i++;
	    document.getElementById("teams").appendChild(newdiv);
          }
	</script>
    </head>
    <body>
        <form method="POST">
	    Team Name<br>
	    <input type="text" name="name"><br><br>
            School Name<br>
	    <input type="text" name="school"><br><br>

	    Members 
	    <button id="add" value="Add" onclick="addFields(); return false;">
	      Add</button><br>
	    
	    <div id = "teams">
	        <div id="entry">
		  <input type="text" name="name0" placeholder="Team 0"><br>
		</div>
		<div id="entry">
	          <input type="text" name="name1" placeholder="Team 1"><br>
		</div>
	    </div>
	    <input type="submit" value="Submit" name="create">
	</form>
    </body>
</html>