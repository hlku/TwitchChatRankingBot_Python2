<?php
    include("threshold.php");
	$ch = $_GET["channel"];
    $content = "";
    
    $cr = curl_init();
    curl_setopt($cr, CURLOPT_URL, "put your ranks files URL here" . $ch . ".rk");
    curl_setopt($cr, CURLOPT_HEADER, 0);
    curl_setopt($cr, CURLOPT_RETURNTRANSFER,1);
    $content = curl_exec($cr);
    $status = curl_getinfo($cr, CURLINFO_HTTP_CODE); 
    curl_close($cr);

    if ($status != 200) echo "<big>這台沒有yourbotname！</big>";
    else {
    $content = json_decode($content);
	$data = $content->data;
?>
<html lang="zh-tw">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Online PHP Script Execution</title>
		
		<!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
		<!-- Latest compiled and minified JavaScript -->
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
		
		<style>
        .table {
            border-radius: 5px;
            width: 50%;
            margin: 0px auto;
            float: none;
        }
        .table tr {
            text-align: center;
        }
        .custom{
            width:50%;
            max-width:50%;
        }
        .room{
            vertical-align: middle;
        }
		</style>
    </head>
    <body>
	<h1 class="text-center"><?php echo $ch; ?>台等級</h1>
    <div class="table-responsive">
		<table class="table table-bordered table-hover custom">
			<thead>
				<tr>
					<th class="text-center">名次</th>
					<th class="text-center">帳號</th>
					<th class="text-center">經驗值 / 升等值</th>
					<th class="text-center">等級</th>
				</tr>
			</thead>
			<tbody><?php
			foreach ($data as $u) {
				$tr = "<tr align=\"center\" bgcolor=";
                
                if ($u[3] < 1) $tr .= "white";
                else if ($u[3] < 6) $tr .= "#FAF0E6";
                else if ($u[3] < 11) $tr .= "#FFFFE0";
                else if ($u[3] < 16) $tr .= "#FFEFD5";
                else if ($u[3] < 21) $tr .= "#FFDAB9";
                else if ($u[3] < 26) $tr .= "#F5DEB3";
                else if ($u[3] < 31) $tr .= "#FFFF00";
                else if ($u[3] < 36) $tr .= "#FFD700";
                else if ($u[3] < 41) $tr .= "#F0E68C";
                else if ($u[3] < 46) $tr .= "#ADFF2F";
                else if ($u[3] < 51) $tr .= "#98FB98";
                else if ($u[3] < 56) $tr .= "#7FFFD4";
                else if ($u[3] < 61) $tr .= "#00FFFF";
                else if ($u[3] < 66) $tr .= "#00BFFF";
                else if ($u[3] < 71) $tr .= "#DDA0DD";
                else if ($u[3] < 76) $tr .= "#FF69B4";
                else if ($u[3] < 81) $tr .= "#FF7F50";
                else if ($u[3] < 86) $tr .= "#FA8072";
                else if ($u[3] < 91) $tr .= "#FF0000";
                else $tr .= "#000000";

                $tr .= ">";
                echo $tr;
				echo "<td class=\"center\">".$u[0]."</td>";
				echo "<td class=\"center\"><a href=\"https://www.twitch.tv/".$u[1]."\" target=\"_blank\">".$u[1]."</td>";
				echo "<td class=\"center\">".$u[2]."/".$th[$u[3]]."</td>";
				$u3 = "<td class=\"center\"><big>";
                if ($u[3] > 90) $u3 .= "<font color=white>".$u[3]."</font>";
                $u3 .= $u[3]."</big></td>";
                echo $u3;
				echo "</tr>";
			}
			?>
			</tbody>
		</table>
    </div>
    </body>
</html>
<?php } ?>
