<?php
	if(isset($_POST['action']) && !empty($_POST['action'])) {
		$action = $_POST['action'];
		switch($action) {
			case 'get-all' : getAllDBData();break;
			case 'get-percent' : getPercent();break;
		}
	}
	function getPercent(){
		$servername = "localhost";
		$username = "dltrgwef";
		$password = "RzbFrATtI0fE";
		$databasename = "dltrgwef_trash_status";
		$conn = new mysqli($servername,$username,$password,$databasename);
		$table_name = $_POST['type'];
		if($conn->connect_error)
		{
			die("Connection Failed: ". $conn->connect_error);
		}
		//echo "Connected successfully";
		$sub_type = $_POST['sub_type'];
		$sql = "SELECT Amount FROM $table_name WHERE `Type` = '$sub_type'";
		$sql_full = "SELECT Amount FROM $table_name WHERE `Type` = 'full'";
		$sql_none = "SELECT Amount FROM $table_name WHERE `Type` = 'none'";

		$result = floatval($conn->query($sql)->fetch_assoc()['Amount']);
		$result_full = floatval($conn->query($sql_full)->fetch_assoc()['Amount']);
		$result_none = floatval($conn->query($sql_none)->fetch_assoc()['Amount']);

		if($result != 0){
			$ans = ($result_none - $result)/($result_none - $result_full) * 100.0;
			$ans_inv = 100 - $ans;
			if($ans < 0){
				$ans = 0;
				$ans_inv = 100;
			}
			if($ans_inv < 0){
				$ans = 100;
				$ans_inv = 0;
			}
			if(round($ans,1) < 33){
				$ans = 33;
				$ans_inv = 67;
			}
			else if(round($ans,1) < 50){
				$ans = 67;
				$ans_inv = 33;
			}
			else {
				$ans = 100;
				$ans_inv = 0;
			}
		}
		else {
			$ans = 0;
			$ans_inv = 100;
		}
		echo '["' . round($ans,1) . '","' . round($ans_inv,1) . '","' . $table_name . '","' . $sub_type . '"]';
	}
	function getRecordData(){
		$servername = "localhost";
		$username = "dltrgwef";
		$password = "RzbFrATtI0fE";
		$databasename = "dltrgwef_record";
		$conn = new mysqli($servername,$username,$password,$databasename);
		$table_name = 'total_statistic';
		if($conn->connect_error)
		{
			die("Connection Failed: ". $conn->connect_error);
		}
		//echo "Connected successfully";

		$sql = "SELECT * FROM $table_name";
		$result = $conn->query($sql);

		if ($result->num_rows > 0){
			echo "[";
			$first = 1;
			while($row = $result->fetch_assoc()){
				if($first == 1){
					$first = 0;
				}
				else{
					echo ",";
				}
				echo "[\"" . $row["type"] . "\",\"" . $row["amount"] . "\"]";
			}
			echo "]";
		}
	}
	function getAllDBData(){
		$servername = "localhost";
		$username = "dltrgwef";
		$password = "RzbFrATtI0fE";
		$databasename = "dltrgwef_record";
		$conn = new mysqli($servername,$username,$password,$databasename);
		$table_name = 'log';
		if($conn->connect_error)
		{
			die("Connection Failed: ". $conn->connect_error);
		}
		//echo "Connected successfully";

		$sql = "SELECT * FROM $table_name";
		$result = $conn->query($sql);

		if ($result->num_rows > 0){
			echo "[";
			$first = 1;
			while($row = $result->fetch_assoc()){
				if($first == 1){
					$first = 0;
				}
				else{
					echo ",";
				}
				echo "[\"" . $row["classifier"] . "\",\"" . $row["image"] . "\",\"" . $row["confidence"] . "\",\"" . $row["category"] . "\",\"" . $row["sub_category"] . "\",\"" . $row["date"] . "\"]";
			}
			echo "]";
		}
	}
?>