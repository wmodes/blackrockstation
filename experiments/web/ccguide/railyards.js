const railyardData =
[
	{'state':'Alabama', 'cities': [
		{'city':'Birmingham', 'yards': [	{'yard':'Boyles YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'East Thomas YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Decatur', 'yards': [	{'yard':'Oakworth YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Fairfield', 'yards': [	{'yard':'Ensley YD', 'carrier':'Birmingham Southern', 'notes':''},
		]}, {'city':'Irondale', 'yards': [	{'yard':'Norris YD', 'carrier':'Norfolk Southern', 'notes':''},
		]}, {'city':'Mobile', 'yards': [	{'yard':'Sibert YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Muscle Shoals', 'yards': [	{'yard':'Sheffield YD', 'carrier':'NS', 'notes':''},
		]}
	]},
	{'state':'Alberta', 'cities': [
		{'city':'Edmonton', 'yards': [
			{'yard':'Bissell YD', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Cloverbar YD', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Dunvegan YD', 'carrier':'CN', 'notes':'Railcar Storage'},
			{'yard':'Scotford YD', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Scotford YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'Lambton Park YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'D.L. MacDonald YD', 'carrier':'ETS', 'notes':''},
			{'yard':'McBain YD', 'carrier':'CN', 'notes':'IM'},
			{'yard':'Strathcona YD', 'carrier':'CP', 'notes':'IM, MSH'},
			{'yard':'Walker YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Calgary', 'yards': [
			{'yard':'Alyth YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'Ogden Park', 'carrier':'CP', 'notes':''},
			{'yard':'Shepard YD', 'carrier':'CP', 'notes':'IM'},
			{'yard':'Manchester YD', 'carrier':'CP', 'notes':'MSH, Storage'},
			{'yard':'Keith YD', 'carrier':'CP', 'notes':'MSH, Storage'},
			{'yard':'Sarcee YD', 'carrier':'CN', 'notes':'IM, MSH'},
			{'yard':'Calgary Logistics Park', 'carrier':'CN', 'notes':'MSH, IM, industry servicing'},
			{'yard':'Anderson Garage', 'carrier':'Calgary Transit', 'notes':''},
			{'yard':'Oliver Bowen Maintenance Centre', 'carrier':'Calgary Transit', 'notes':''},
		]}, {'city':'Lethbridge', 'yards': [
			{'yard':'Kipp YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'Churchill Industrial YD', 'carrier':'CP', 'notes':'MSH'},
		]}, {'city':'Medicine Hat', 'yards': [
			{'yard':'Medicine Hat YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'Dunmore YD', 'carrier':'CP', 'notes':'MSH'},
		]}
	]},
	{'state':'Arkansas', 'cities': [
		{'city':'North Little Rock', 'yards': [	{'yard':'North Little Rock YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Pine Bluff', 'yards': [	{'yard':'Pine Bluff YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Marion', 'yards': [	{'yard':'Marion Intermodal Terminal', 'carrier':'UP', 'notes':''},
		]}
	]},
	{'state':'British Columbia', 'cities': [
		{'city':'Nanaimo', 'yards': [
			{'yard':'Wellcox YD', 'carrier':'SVI', 'notes':'MSH, Barge operation'},
		]}, {'city':'Vancouver', 'yards': [
			{'yard':'Coquitlam YD', 'carrier':'CP', 'notes':'IM, MSH'},
			{'yard':'Mayfair Intermodal', 'carrier':'CP', 'notes':'IM'},
			{'yard':'Williston YD', 'carrier':'CP', 'notes':'IM, Grain'},
			{'yard':'Thornton YD', 'carrier':'CN', 'notes':'IM, MSH'},
			{'yard':'North Vancouver YD', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Lulu Island YD', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Trapp YD', 'carrier':'SRY', 'notes':'MSH'},
			{'yard':'New YD', 'carrier':'BNSF', 'notes':'MSH'},
			{'yard':'Glen YD', 'carrier':'BNSF', 'notes':'MSH'},
			{'yard':'Main YD', 'carrier':'BNSF', 'notes':'MSH'},
			{'yard':'Vancouver Reliability Center', 'carrier':'VIA', 'notes':'Coach YD & Shop'},
		]}, {'city':'Kamloops', 'yards': [
			{'yard':'Kamloops CP YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'Kamloops CN YD', 'carrier':'CN', 'notes':'IM, MSH'},
		]}, {'city':'Golden', 'yards': [
			{'yard':'Golden YD', 'carrier':'CP', 'notes':'MSH, Coal Staging YD'},
		]}, {'city':'Trail', 'yards': [
			{'yard':'Tadanac YD', 'carrier':'CP', 'notes':'MSH'},
		]}, {'city':'Cranbrook', 'yards': [
			{'yard':'Cranbrook YD', 'carrier':'CP', 'notes':'MSH'},
	]} ]},
	{'state':'California', 'cities': [
		{'city':'Barstow', 'yards': [	{'yard':'Barstow YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'City of Industry', 'yards': [	{'yard':'Industry YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Colton', 'yards': [	{'yard':'West Colton YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Commerce', 'yards': [	{'yard':'East YD', 'carrier':'UP', 'notes':''},
			{'yard':'Hobart YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Fresno', 'yards': [	{'yard':'Calwa YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Los Angeles', 'yards': [	{'yard':'Aurant YD', 'carrier':'UP', 'notes':''},
			{'yard':'East Los Angeles YD', 'carrier':'UP', 'notes':''},
			{'yard':'Piggyback YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Oakland', 'yards': [	{'yard':'Desert YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Roseville', 'yards': [	{'yard':'J.R. Davis YD', 'carrier':'UP', 'notes':'largest on the west coast'},
		]}
	]},
	{'state':'Colorado', 'cities': [
		{'city':'Denver', 'yards': [	{'yard':'36th Street YD', 'carrier':'UP', 'notes':''},
			{'yard':'Globeville YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'North YD', 'carrier':'UP', 'notes':'former DRGW'},
			{'yard':'Rennix YD', 'carrier':'BNSF', 'notes':'IM'},
		]}
	]},
	{'state':'Connecticut', 'cities': [
		{'city':'New Haven', 'yards': [	{'yard':'Cedar Hill YD', 'carrier':'CSXT/P & W/Connecticut Southern/Amtrak', 'notes':''},
		]}, {'city':'Hartford', 'yards': [	{'yard':'Hartford YD', 'carrier':'CSO/PAR', 'notes':''},
		]}
	]},
	{'state':'Delaware', 'cities': [
		{'city':'Wilmington', 'yards': [	{'yard':'Edgemoor YD', 'carrier':'NS', 'notes':''},
			{'yard':'Elsmere YD', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'District of Columbia', 'cities': [
		{'city':'Washington', 'yards': [	{'yard':'Ivy City YD', 'carrier':'Amtrak', 'notes':''},
			{'yard':'Benning YD', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'Florida', 'cities': [
		{'city':'Bradenton', 'yards': [	{'yard':'Tropicana YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Fort Pierce', 'yards': [	{'yard':'Fort Pierce YD', 'carrier':'Florida East Coast', 'notes':''},
		]}, {'city':'Hialeah', 'yards': [	{'yard':'Hialeah YD', 'carrier':'CSXT/Tri-Rail/Amtrak', 'notes':''},
		]}, {'city':'Jacksonville', 'yards': [	{'yard':'Bowden YD', 'carrier':'Florida East Coast', 'notes':''},
			{'yard':'Moncrief YD', 'carrier':'CSXT', 'notes':'former Seaboard Coast Line'},
			{'yard':'Simpson YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Lakeland', 'yards': [	{'yard':'Winston YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'New Smyrna Beach', 'yards': [	{'yard':'New Smyrna Beach YD', 'carrier':'Florida East Coast', 'notes':''},
		]}, {'city':'Miami', 'yards': [	{'yard':'Hialeah YD', 'carrier':'Florida East Coast', 'notes':''},
		]}, {'city':'Orlando', 'yards': [	{'yard':'Taft YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Tampa', 'yards': [	{'yard':'Rockport YD, Uceta YD, & Yeoman YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Winter Haven', 'yards': [	{'yard':'Central Florida Intermodal Logistics Center', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'Georgia', 'cities': [
		{'city':'Albany', 'yards': [	{'yard':'Atlantic Coast Line YD', 'carrier':'GFRR', 'notes':''},
			{'yard':'Albany Central of Georgia YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Atlanta', 'yards': [	{'yard':'Tilford YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Hulsey YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Inman YD', 'carrier':'NS', 'notes':''},
			{'yard':'North Avenue YDs', 'carrier':'', 'notes':''},
			{'yard':'Howell Interlocking', 'carrier':'', 'notes':''},
		]}, {'city':'Austell', 'yards': [	{'yard':'John W. Whitaker Intermodal Terminal', 'carrier':'Norfolk Southern', 'notes':''},
		]}, {'city':'Fairburn', 'yards': [	{'yard':'Fairburn YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Macon', 'yards': [	{'yard':'Brosnan YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Rome', 'yards': [	{'yard':'Forestville YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Valdosta', 'yards': [	{'yard':'Langdale YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Waycross', 'yards': [	{'yard':'Waycross Rice YD', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'Idaho', 'cities': [
		{'city':'Bonner’s Ferry', 'yards': [	{'yard':'Bonner’s Ferry YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Eastport', 'yards': [	{'yard':'Eastport YD', 'carrier':'UP/CP', 'notes':''},
		]}, {'city':'Hauser', 'yards': [	{'yard':'Hauser YD', 'carrier':'BNSF/MRL', 'notes':''},
		]}, {'city':'Idaho Falls', 'yards': [	{'yard':'Idaho Falls YD', 'carrier':'UP/EIRR', 'notes':''},
		]}, {'city':'Minidoka', 'yards': [	{'yard':'Minidoka YD', 'carrier':'UP/EIRR', 'notes':''},
		]}, {'city':'Nampa', 'yards': [	{'yard':'Nampa YD', 'carrier':'UP/BVRR', 'notes':''},
		]}, {'city':'Plummer', 'yards': [	{'yard':'Plummer YD', 'carrier':'STMA/UP', 'notes':''},
		]}, {'city':'Pocatello', 'yards': [	{'yard':'Pocatello YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Sandpoint', 'yards': [	{'yard':'Boyer YD', 'carrier':'BNSF/UP/POVA', 'notes':''},
		]}, {'city':'St Marie’s', 'yards': [	{'yard':'St Maries YD', 'carrier':'STMA', 'notes':''},
		]}, {'city':'Twin Falls', 'yards': [	{'yard':'Twin Falls YD', 'carrier':'Eastern Idaho HQ', 'notes':'Watco; former UP interchange YD'},
		]}
	]},
	{'state':'Illinois', 'cities': [
		{'city':'Champaign', 'yards': [	{'yard':'Champaign YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Chicago area', 'yards': [
			{'yard':'14th Street Coach YD', 'carrier':'Metra', 'notes':''},
			{'yard':'47th Street YD', 'carrier':'NS', 'notes':'IM'},
			{'yard':'59th Street YD', 'carrier':'CSXT', 'notes':'IM, switched by Chicago Rail Link'},
			{'yard':'Ashland Avenue YD', 'carrier':'NS', 'notes':'cars'},
			{'yard':'Aurora', 'carrier':'Metra commuter coach YD for BNSF route', 'notes':''},
			{'yard':'Barr YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Bedford Park YD', 'carrier':'CSXT', 'notes':'IM, switched by Chicago Rail Link'},
			{'yard':'Bensenville YD', 'carrier':'CP', 'notes':''},
			{'yard':'Blue Island YD', 'carrier':'Indiana Harbor Belt', 'notes':''},
			{'yard':'Burnham YD', 'carrier':'South Shore Freight', 'notes':''},
			{'yard':'Burr Oak YD', 'carrier':'Iowa Interstate / Chicago Rail Link', 'notes':''},
			{'yard':'California Ave Coach YDs', 'carrier':'UP', 'notes':''},
			{'yard':'Calumet YD', 'carrier':'NS', 'notes':''},
			{'yard':'Clearing YD', 'carrier':'BRC', 'notes':'Hump YD, IM. MSH'},
			{'yard':'Cicero YD', 'carrier':'BNSF', 'notes':'IM'},
			{'yard':'Commercial Avenue YD', 'carrier':'BRC', 'notes':''},
			{'yard':'Corwith YDs', 'carrier':'BNSF', 'notes':'IM'},
			{'yard':'East Joliet YD aka Elgin', 'carrier':'CN', 'notes':'former Joliet & Eastern'},
			{'yard':'Eola YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Glenn YD', 'carrier':'CN', 'notes':''},
			{'yard':'Global I', 'carrier':'UP', 'notes':'IM'},
			{'yard':'Global II', 'carrier':'UP', 'notes':'IM'},
			{'yard':'Global III', 'carrier':'UP', 'notes':'IM'},
			{'yard':'Global IV', 'carrier':'UP', 'notes':'IM'},
			{'yard':'Markham YD', 'carrier':'CN', 'notes':''},
			{'yard':'Irondale YD', 'carrier':'Chicago Rail Link', 'notes':''},
			{'yard':'Landers YD', 'carrier':'NS', 'notes':'IM'},
			{'yard':'Logistics Park', 'carrier':'BNSF', 'notes':'IM'},
			{'yard':'Proviso YD', 'carrier':'UP Hump YD', 'notes':'IM, MSH'},
			{'yard':'Schiller Park YD', 'carrier':'CN', 'notes':''},
			{'yard':'South Chicago YD', 'carrier':'South Chicago & Indiana Harbor', 'notes':''},
			{'yard':'Western Avenue (Metra commuter coach YDs)', 'carrier':'UP/Milwaukee Road', 'notes':'former C&NW'},
			{'yard':'Willow Springs', 'carrier':'BNSF', 'notes':'IM'},
			{'yard':'YD Center', 'carrier':'UP', 'notes':''},
		]}, {'city':'Decatur', 'yards': [	{'yard':'Decatur YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Dupo', 'yards': [	{'yard':'Dupo YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'East Peoria', 'yards': [	{'yard':'East Peoria YD', 'carrier':'TZPR', 'notes':''},
			{'yard':'East Peoria YD (Toledo)', 'carrier':'Peoria & Western', 'notes':''},
		]}, {'city':'East Saint Louis', 'yards': [	{'yard':'Gateway YD 64', 'carrier':'Alton & Southern', 'notes':'Hump YD'},
		]}, {'city':'Galesburg', 'yards': [	{'yard':'Galesburg YD', 'carrier':'BNSF', 'notes':'Hump YD'},
		]}, {'city':'Havana', 'yards': [	{'yard':'Quiver YD', 'carrier':'Illinois & Midland', 'notes':''},
		]}, {'city':'Kankakee', 'yards': [	{'yard':'Kankakee YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Madison', 'yards': [	{'yard':'Madison YD', 'carrier':'TRRA', 'notes':''},
		]}, {'city':'Ottawa', 'yards': [	{'yard':'Fremont Street YD', 'carrier':'IR', 'notes':''},
		]}, {'city':'Pekin', 'yards': [	{'yard':'Powerton YD', 'carrier':'Illinois & Midland', 'notes':''},
		]}, {'city':'Silvis', 'yards': [	{'yard':'Silvis YD', 'carrier':'Iowa Interstate', 'notes':''},
		]}, {'city':'Springfield', 'yards': [	{'yard':'Shops YD', 'carrier':'Illinois & Midland', 'notes':''},
		]}
	]},
	{'state':'Indiana', 'cities': [
		{'city':'Avon', 'yards': [	{'yard':'Avon YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Elkhart', 'yards': [	{'yard':'Elkhart Young YD (72+15)', 'carrier':'NS', 'notes':''},
		]}, {'city':'Fort Wayne', 'yards': [	{'yard':'Fort Wayne YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Gary', 'yards': [	{'yard':'Kirk YD (Elgin)', 'carrier':'CN', 'notes':'former Joliet & Eastern'},
		]}, {'city':'Hammond', 'yards': [	{'yard':'Gibson YD', 'carrier':'Indiana Harbor Belt', 'notes':''},
		]}, {'city':'Indianapolis', 'yards': [	{'yard':'Hawthorne YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Jeffersonville', 'yards': [	{'yard':'Jeff YD', 'carrier':'Louisville & Indiana', 'notes':''},
		]}
	]},
	{'state':'Iowa', 'cities': [
		{'city':'Council Bluffs', 'yards': [	{'yard':'Council Bluffs YD', 'carrier':'Iowa Interstate & UP', 'notes':''},
		]}, {'city':'Davenport', 'yards': [	{'yard':'Nahant YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Des Moines', 'yards': [	{'yard':'Short Line YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Mason City', 'yards': [	{'yard':'Mason City YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'South Amana', 'yards': [	{'yard':'South Amana', 'carrier':'Iowa Interstate', 'notes':''},
		]}, {'city':'Waterloo', 'yards': [	{'yard':'Waterloo YD', 'carrier':'CN', 'notes':''},
		]}
	]},
	{'state':'Kansas', 'cities': [
		{'city':'Kansas City', 'yards': [	{'yard':'Argentine YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Armourdale YD', 'carrier':'UP', 'notes':''},
			{'yard':'Mill Street YD (KCT)', 'carrier':'Kaw River', 'notes':'formerly Gateway Western RR'},
		]}
	]},
	{'state':'Kentucky', 'cities': [
		{'city':'Louisville', 'yards': [	{'yard':'Prime F. Osborn YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Youngtown YD', 'carrier':'NS', 'notes':''},
			{'yard':'Oak Street YD', 'carrier':'Paducah & Louisville', 'notes':''},
		]}, {'city':'Danville', 'yards': [	{'yard':'Danville YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Ludlow', 'yards': [	{'yard':'Ludlow YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Russell', 'yards': [	{'yard':'Russell YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Corbin', 'yards': [	{'yard':'Corbin YD', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'Louisiana', 'cities': [
		{'city':'Alexandria:', 'yards': [
			{'yard':'Alexandria YD', 'carrier':'KCS', 'notes':''},
			{'yard':'Alexandria YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Baton Rouge area:', 'yards': [
			{'yard':'Addis YD', 'carrier':'UP', 'notes':''},
			{'yard':'Baton Rouge YD', 'carrier':'CN', 'notes':''},
			{'yard':'Baton Rouge YD', 'carrier':'KCS', 'notes':''},
			{'yard':'Geismar YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Lafayette:', 'yards': [
			{'yard':'Lafayette North YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Lafayette South YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Lake Charles area:', 'yards': [
			{'yard':'Edgerly Plastic YD', 'carrier':'UP', 'notes':''},
			{'yard':'Lake Charles YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Livonia', 'yards': [	{'yard':'Livonia YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'New Orleans area:', 'yards': [
			{'yard':'Avondale YD', 'carrier':'BNSF/UP', 'notes':''},
			{'yard':'Destrahan YD', 'carrier':'CN', 'notes':''},
			{'yard':'France YD', 'carrier':'NOPB', 'notes':''},
			{'yard':'Gentilly YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Mays YD', 'carrier':'CN', 'notes':''},
			{'yard':'New Orleans YD', 'carrier':'KCS', 'notes':''},
			{'yard':'Oliver YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Ottawa', 'yards': [
			{'yard':'Deramus YD', 'carrier':'KCS', 'notes':''},
		]}
	]},
	{'state':'Maine', 'cities': [
		{'city':'Auburn:', 'yards': [
			{'yard':'Danville Junction', 'carrier':'PAR/St. Lawrence & Atlantic', 'notes':''},
			{'yard':'Lewiston Junction', 'carrier':'St. Lawrence & Atlantic', 'notes':''},
		]}, {'city':'Bangor', 'yards': [	{'yard':'Bangor YD', 'carrier':'PAR', 'notes':''},
		]}, {'city':'Brownville', 'yards': [	{'yard':'Brownville Junction', 'carrier':'Eastern Maine/CP', 'notes':''},
		]}, {'city':'Brunswick', 'yards': [	{'yard':'Brunswick YD', 'carrier':'PAR/Amtrak/Maine Dept of Trans.', 'notes':''},
		]}, {'city':'Hermon', 'yards': [	{'yard':'Northern Maine Junction', 'carrier':'PAR/CP', 'notes':''},
		]}, {'city':'Mattawamkeag', 'yards': [	{'yard':'Mattawamkeag YD', 'carrier':'PAR/Eastern Maine', 'notes':''},
		]}, {'city':'Millinocket', 'yards': [	{'yard':'Millinocket YD', 'carrier':'Maine Northern/CP', 'notes':''},
		]}, {'city':'Portland:', 'yards': [
			{'yard':'YD 8', 'carrier':'PAR/Maine International', 'notes':'Marine Terminal'},
			{'yard':'YD 10', 'carrier':'PAR/Amtrak', 'notes':''},
			{'yard':'YD 11', 'carrier':'PAR', 'notes':''},
		]}, {'city':'Rockland', 'yards': [	{'yard':'Rockland YD', 'carrier':'Maine Dept of Transportation', 'notes':''},
		]}, {'city':'Rumford', 'yards': [	{'yard':'Rumford YD', 'carrier':'PAR', 'notes':''},
		]}, {'city':'South Portland:', 'yards': [
			{'yard':'Rigby YD', 'carrier':'PAR', 'notes':''},
			{'yard':'YD 3', 'carrier':'PAR/Turner’s Island', 'notes':''},
			{'yard':'YD 6', 'carrier':'PAR', 'notes':''},
		]}, {'city':'Waterville', 'yards': [	{'yard':'Waterville Shops', 'carrier':'PAR', 'notes':''},
		]}, {'city':'Westbrook', 'yards': [	{'yard':'YD 12', 'carrier':'PAR', 'notes':''},
		]}
	]},
	{'state':'Manitoba', 'cities': [
		{'city':'Winnipeg', 'yards': [
			{'yard':'Burlington Northern Santa Fe Manitoba YD', 'carrier':'BNSF Manitoba', 'notes':''},
			{'yard':'East YD', 'carrier':'CN', 'notes':''},
			{'yard':'Fort Rouge YD', 'carrier':'CN', 'notes':''},
			{'yard':'Greater Winnipeg Water District St. Boniface YD', 'carrier':'GWWDR', 'notes':''},
			{'yard':'North Transcona YD', 'carrier':'CP', 'notes':''},
			{'yard':'Central Manitoba Railway YD', 'carrier':'CEMR', 'notes':''},
			{'yard':'St. Boniface YD', 'carrier':'CPR', 'notes':''},
			{'yard':'Symington YD', 'carrier':'CN', 'notes':'IM, Hump YD'},
			{'yard':'Transcona YD', 'carrier':'CN', 'notes':''},
			{'yard':'Winnipeg YD', 'carrier':'CP', 'notes':'IM, Hump YD'},
		]}
	]},
	{'state':'Maryland', 'cities': [
		{'city':'Baltimore', 'yards': [
			{'yard':'Bayview YDs', 'carrier':'CSXT & NS', 'notes':''},
			{'yard':'Canton/Coal YD', 'carrier':'NS', 'notes':''},
			{'yard':'Penn Mary YD', 'carrier':'CTN', 'notes':''},
		]}, {'city':'Cumberland', 'yards': [	{'yard':'Cumberland YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Hagerstown', 'yards': [	{'yard':'Hagerstown Terminal', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'Massachusetts', 'cities': [
		{'city':'Boston:', 'yards': [
			{'yard':'Beacon Park YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Boston Engine Terminal', 'carrier':'MBTA', 'notes':''},
			{'yard':'Southampton Street YD', 'carrier':'MBTA/Amtrak', 'notes':''},
			{'yard':'Readville', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Ayer', 'yards': [	{'yard':'Hill YD', 'carrier':'PAR', 'notes':''},
		]}, {'city':'East Deerfield', 'yards': [	{'yard':'East Deerfield', 'carrier':'Pan Am', 'notes':''},
		]}, {'city':'Fitchburg', 'yards': [	{'yard':'Fitchburg', 'carrier':'Pan Am', 'notes':''},
		]}, {'city':'Framingham', 'yards': [	{'yard':'North YD / Nevins YDs', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Gardner', 'yards': [	{'yard':'', 'carrier':'Pan Am/PW', 'notes':''},
		]}, {'city':'Lawrence', 'yards': [	{'yard':'', 'carrier':'Pan Am', 'notes':''},
		]}, {'city':'Lowell', 'yards': [	{'yard':'', 'carrier':'Pan Am', 'notes':''},
		]}, {'city':'Palmer', 'yards': [	{'yard':'', 'carrier':'NECR/MCER/CSXT', 'notes':''},
		]}, {'city':'West Springfield', 'yards': [	{'yard':'', 'carrier':'CSXT/CSOR', 'notes':''},
		]}, {'city':'Worcester', 'yards': [	{'yard':'', 'carrier':'CSXT/PW', 'notes':''},
		]}
	]},
	{'state':'Michigan', 'cities': [
		{'city':'Battle Creek', 'yards': [	{'yard':'Battle Creek YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Detroit', 'yards': [	{'yard':'Livernois YD - aka Junction YD', 'carrier':'CSXT & NS', 'notes':''},
		]}, {'city':'Grand Rapids', 'yards': [	{'yard':'Hugart YD', 'carrier':'GDLK', 'notes':'Took over for NS in 2009'},
		]}, {'city':'Flint', 'yards': [	{'yard':'South YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Flat Rock', 'yards': [	{'yard':'Flat Rock YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Kalamazoo', 'yards': [	{'yard':'Gearhart YD', 'carrier':'GDLK', 'notes':'Took over for NS in 2009'},
		]}, {'city':'Lansing', 'yards': [	{'yard':'Cory YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Pontiac', 'yards': [	{'yard':'Pontiac YD', 'carrier':'', 'notes':''},
		]}, {'city':'Wyoming', 'yards': [	{'yard':'Wyoming YD', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'Minnesota', 'cities': [
		{'city':'Duluth', 'yards': [	{'yard':'Proctor YD', 'carrier':'CN', 'notes':''},
			{'yard':'Rice’s Point YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Rice’s Point YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Minneapolis', 'yards': [	{'yard':'Humboldt YD', 'carrier':'CP', 'notes':''},
			{'yard':'Northtown YD 55', 'carrier':'BNSF', 'notes':''},
			{'yard':'Shoreham YDs', 'carrier':'CP', 'notes':''},
		]}, {'city':'Northfield', 'yards': [	{'yard':'Northfield YD', 'carrier':'UP/CP/PGR', 'notes':''},
		]}, {'city':'Ranier', 'yards': [	{'yard':'Ranier YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'St. Paul', 'yards': [	{'yard':'Midway YD', 'carrier':'MN Comm.', 'notes':''},
			{'yard':'Pig’s Eye YD', 'carrier':'CP', 'notes':''},
			{'yard':'Hoffman YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'South St. Paul', 'yards': [	{'yard':'South St. Paul YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Valley Park', 'yards': [	{'yard':'Valley Park YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Virginia', 'yards': [	{'yard':'Virginia YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Waseca', 'yards': [	{'yard':'Waseca YD', 'carrier':'CP', 'notes':''},
		]}
	]},
	{'state':'Missouri', 'cities': [
		{'city':'Kansas City', 'yards': [	{'yard':'Neff YD 42', 'carrier':'UP', 'notes':''},
			{'yard':'Knoche/Joint Agency YD', 'carrier':'KCS/CP', 'notes':''},
			{'yard':'Kansas City SmartPort', 'carrier':'KCS', 'notes':'IM, autos'},
			{'yard':'North Kansas City Avondale YD', 'carrier':'NS', 'notes':''},
			{'yard':'Birmingham', 'carrier':'NS', 'notes':'IM, autos'},
		]}, {'city':'North Kansas City', 'yards': [	{'yard':'Murray YD', 'carrier':'BNSF', 'notes':'bulk commodities marshaling terminal; former Hump'},
		]}, {'city':'St. Louis', 'yards': [	{'yard':'Chouteau YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Springfield', 'yards': [	{'yard':'North Springfield YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'South Springfield YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Springfield YD', 'carrier':'BNSF', 'notes':''},
		]}
	]},
	{'state':'Nebraska', 'cities': [
		{'city':'Lincoln', 'yards': [
			{'yard':'Havelock YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Hobson YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'North Platte', 'yards': [	{'yard':'Bailey YD 64+50', 'carrier':'UP', 'notes':'The largest YD in the world'},
		]}
	]},
	{'state':'Nevada', 'cities': [
		{'city':'Elko', 'yards': [	{'yard':'Elko YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Las Vegas', 'yards': [	{'yard':'Arden YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Sparks', 'yards': [	{'yard':'Sparks YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Winnemucca', 'yards': [	{'yard':'Winnemucca YD', 'carrier':'UP', 'notes':''},
		]}
	]},
	{'state':'New Brunswick', 'cities': [
		{'city':'Moncton', 'yards': [
			{'yard':'Gordon YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Saint John', 'yards': [
			{'yard':'Island YD', 'carrier':'CN/NBSR', 'notes':'MSH/IM'},
			{'yard':'Dever Rd. YD', 'carrier':'NBSR', 'notes':'MSH'},
		]}
	]},
	{'state':'New Hampshire', 'cities': [
		{'city':'Berlin', 'yards': [	{'yard':'Berlin YD', 'carrier':'SLR', 'notes':''},
		]}, {'city':'Concord', 'yards': [	{'yard':'Concord YD', 'carrier':'NES', 'notes':'New Hampshire Central Railroad'},
		]}, {'city':'Conway', 'yards': [	{'yard':'North Conway Depot & RR YD', 'carrier':'Conway Scenic', 'notes':''},
		]}, {'city':'Dover', 'yards': [	{'yard':'Dover YD', 'carrier':'PAR', 'notes':'New Hampshire Northcoast Railroad'},
		]}, {'city':'Nashua', 'yards': [	{'yard':'Nashua YD', 'carrier':'PAR', 'notes':''},
		]}
	]},
	{'state':'New Jersey', 'cities': [
		{'city':'Camden', 'yards': [	{'yard':'Pavonia YD 32', 'carrier':'CSXT & NS', 'notes':''},
		]}, {'city':'Jersey City:', 'yards': [
			{'yard':'Croxton YD', 'carrier':'NS', 'notes':''},
			{'yard':'Greenville YD', 'carrier':'Port Jersey', 'notes':''},
		]}, {'city':'Kearny', 'yards': [	{'yard':'South Kearney Terminal', 'carrier':'CSXT', 'notes':''},
			{'yard':'Linden YD', 'carrier':'SIR', 'notes':''},
			{'yard':'Little Ferry YD', 'carrier':'CSXT/NYSW/CSAO', 'notes':''},
		]}, {'city':'Newark', 'yards': [	{'yard':'Oak Island YD', 'carrier':'CSXT/NS', 'notes':''},
			{'yard':'North Bergen YD', 'carrier':'CSXT & NYSW', 'notes':''},
		]}
	]},
	{'state':'New York', 'cities': [
		{'city':'Binghamton', 'yards': [	{'yard':'East Binghamton YD', 'carrier':'NS', 'notes':''},
			{'yard':'Middle YD', 'carrier':'NS', 'notes':''},
			{'yard':'Bevier Street YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Buffalo:', 'yards': [
			{'yard':'Bison YD', 'carrier':'NS', 'notes':''},
			{'yard':'Black Rock Rail YD', 'carrier':'CN', 'notes':''},
			{'yard':'Frontier YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'East Syracuse', 'yards': [	{'yard':'De Witt YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Mechanicville', 'yards': [	{'yard':'Mechanicville', 'carrier':'PAS', 'notes':'IM'},
		]}, {'city':'New York City', 'yards': [
			{'yard':'Arlington YD', 'carrier':'Staten Island', 'notes':''},
			{'yard':'High Bridge Facility', 'carrier':'Metro-North', 'notes':'Passenger & Maintenance YD'},
			{'yard':'Hillside Facility', 'carrier':'LIRR', 'notes':'Passenger YD'},
			{'yard':'Oak Point YD', 'carrier':'CSXT', 'notes':'MSH'},
			{'yard':'Sunnyside YD', 'carrier':'Amtrak', 'notes':'NJ Transit Passenger YD'},
			{'yard':'West Side YD', 'carrier':'LIRR', 'notes':'Passenger YD'},
		]}, {'city':'Rochester', 'yards': [
			{'yard':'Brooks Avenue YD', 'carrier':'Rochester & Southern', 'notes':''},
			{'yard':'Goodman Street YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Selkirk', 'yards': [	{'yard':'Selkirk YD', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'North Carolina', 'cities': [
		{'city':'Charlotte', 'yards': [	{'yard':'Charlotte YD', 'carrier':'NS', 'notes':''},
			{'yard':'Pinoca YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Hamlet', 'yards': [	{'yard':'Hamlet YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Linwood', 'yards': [	{'yard':'Spencer YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Raleigh', 'yards': [	{'yard':'Glenwood YD', 'carrier':'NS', 'notes':''},
		]}
	]},
	{'state':'North Dakota', 'cities': [
		{'city':'Enderlin', 'yards': [	{'yard':'Enderlin YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Harvey', 'yards': [	{'yard':'Harvey YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Mandan', 'yards': [	{'yard':'Mandan YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Minot', 'yards': [	{'yard':'Gavin YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Minot YD', 'carrier':'CP', 'notes':''},
		]}
	]},
	{'state':'Nova Scotia', 'cities': [
		{'city':'Halifax', 'yards': [
			{'yard':'Rockingham YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Truro', 'yards': [	{'yard':'Truro YD', 'carrier':'CN/CBNS', 'notes':'MSH'},
		]}, {'city':'Stellarton', 'yards': [	{'yard':'Stellarton YD', 'carrier':'CBNS', 'notes':'MSH'},

		]}
	]},
	{'state':'Ohio', 'cities': [
		{'city':'Bellevue', 'yards': [	{'yard':'Bellevue YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Cincinnati', 'yards': [	{'yard':'June Street YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Queensgate YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Storrs YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Gest Street YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Cleveland', 'yards': [	{'yard':'Collinwood YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Rockport YD', 'carrier':'NS', 'notes':''},
			{'yard':'Clark Avenue YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Columbus', 'yards': [	{'yard':'Buckeye YD East Side Of YD Intermode', 'carrier':'CSXT/NS', 'notes':'Storage Only & Local Interchange w/ Camp Chase Industrial Railroad'},
			{'yard':'Columbus YD, Corr Road', 'carrier':'CSXT', 'notes':''},
			{'yard':'Parsons YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Watkins YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Dayton', 'yards': [	{'yard':'Needmore YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Fairfield', 'yards': [	{'yard':'Wayne YD', 'carrier':'CSXT', 'notes':'Closed'},
		]}, {'city':'Hamilton', 'yards': [	{'yard':'South Hamilton YD', 'carrier':'CSXT', 'notes':'Closed 1988'},
			{'yard':'Woods YD', 'carrier':'CSXT', 'notes':'Closed 2013'},
		]}, {'city':'Lima', 'yards': [	{'yard':'South Lima YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Mariemont', 'yards': [	{'yard':'Clare YD', 'carrier':'CET/NS', 'notes':''},
		]}, {'city':'Middletown', 'yards': [	{'yard':'Reed YD', 'carrier':'AK Steel', 'notes':''},
			{'yard':'New Reeds YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Moraine', 'yards': [	{'yard':'Moraine YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Newark', 'yards': [	{'yard':'Ohio Central Rail YD Newark', 'carrier':'OHCR', 'notes':''},
		]}, {'city':'New Miami', 'yards': [	{'yard':'New River YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'North Baltimore', 'yards': [	{'yard':'North Baltimore Intermodal YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'North Excello', 'yards': [	{'yard':'Lind YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Norwood', 'yards': [	{'yard':'McCullough YD', 'carrier':'IORY', 'notes':''},
		]}, {'city':'Sharonville', 'yards': [	{'yard':'Sharon YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Toledo', 'yards': [	{'yard':'Air Line YD', 'carrier':'NS', 'notes':''},
			{'yard':'Stanley YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Walbridge YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Willard', 'yards': [	{'yard':'Willard YD', 'carrier':'CSXT)', 'notes':''},
		]}
	]},
	{'state':'Oklahoma', 'cities': [
		{'city':'Alva', 'yards': [	{'yard':'Alva YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Oklahoma City', 'yards': [	{'yard':'Harter YD', 'carrier':'UP', 'notes':'former MKT'},
			{'yard':'North YD (aka East YD)', 'carrier':'BN, SLSF', 'notes':'WATCO; former BNSF'},
			{'yard':'Nowers YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'South YD aka Flynn YD', 'carrier':'BNSF', 'notes':'former ATSF'},
		]}, {'city':'Owasso', 'yards': [	{'yard':'Owasso YD', 'carrier':'SLWC/SKOL', 'notes':''},
		]}, {'city':'Tulsa', 'yards': [	{'yard':'Cherokee YD', 'carrier':'BNSF', 'notes':'Hump'},
		]}
	]},
	{'state':'Ontario', 'cities': [
		{'city':'Thunder Bay', 'yards': [
			{'yard':'Thunder Bay YD', 'carrier':'CP', 'notes':'IM, MSH, Grain Staging'},
			{'yard':'Neebing YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Sudbury', 'yards': [
			{'yard':'Sudbury YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'Capreol YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Cambridge', 'yards': [
			{'yard':'Hagey YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Toronto', 'yards': [
			{'yard':'Toronto YD', 'carrier':'CP', 'notes':'MSH, Former Hump YD, Automotive compound'},
			{'yard':'Don YD', 'carrier':'GO', 'notes':'Transit layover facility'},
			{'yard':'North Bathurst YD', 'carrier':'GO', 'notes':'Transit layover facility'},
			{'yard':'Vaughan Intermodal Terminal', 'carrier':'CP', 'notes':'IM'},
			{'yard':'MacMillan YD', 'carrier':'CN', 'notes':'Hump YD'},
			{'yard':'Brampton Intermodal Terminal', 'carrier':'CN', 'notes':'IM'},
			{'yard':'Lambton/West Toronto YDs', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'CPR Parkdale YD', 'carrier':'CVR', 'notes':'MSH, repair YDs'},
			{'yard':'Willowbrook Rail Maintenance Facility', 'carrier':'GO', 'notes':'Transit facility'},
			{'yard':'Whitby Rail Maintenance Facility', 'carrier':'GO', 'notes':'Transit facility'},
			{'yard':'Oakville', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Aldershot', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Hamilton', 'yards': [
			{'yard':'CPR Aberdeen YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'Stuart St. YD', 'carrier':'CN/SOR', 'notes':'MSH'},
			{'yard':'Parkdale YD', 'carrier':'CN/SOR', 'notes':'MSH'},
		]}, {'city':'London', 'yards': [
			{'yard':'Quebec St. YD', 'carrier':'CP', 'notes':'MSH'},
			{'yard':'London YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Sarnia', 'yards': [
			{'yard':'Sarnia YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Englehart', 'yards': [	{'yard':'Englehart YD', 'carrier':'ONR', 'notes':'MSH'},
		]}, {'city':'Ottawa', 'yards': [
			{'yard':'Walkley YD', 'carrier':'CN', 'notes':'MSH'},
		]}
	]},
	{'state':'Oregon', 'cities': [
		{'city':'Eugene', 'yards': [	{'yard':'Eugene YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Hermiston', 'yards': [	{'yard':'Hinkle YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Medford', 'yards': [	{'yard':'Medford YD', 'carrier':'CORP', 'notes':''},
		]}, {'city':'Klamath Falls', 'yards': [
			{'yard':'Klamath Falls YD', 'carrier':'UP', 'notes':''},
			{'yard':'Klamath Falls YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Portland', 'yards': [
			{'yard':'Albina YD', 'carrier':'UP', 'notes':''},
			{'yard':'Barnes YD', 'carrier':'UP', 'notes':'Bulk, Intermodel Terminal'},
			{'yard':'Brooklyn YD', 'carrier':'UP', 'notes':''},
			{'yard':'Willbridge YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Lake YD', 'carrier':'BNSF/UP/PTRC', 'notes':''},
			{'yard':'Terminal 6/East St. John', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Winchester', 'yards': [	{'yard':'Winchester YD', 'carrier':'CORP', 'notes':''},
		]}
	]},
	{'state':'Pennsylvania', 'cities': [
		{'city':'Allentown', 'yards': [	{'yard':'', 'carrier':'NS', 'notes':''},
			{'yard':'Conway YD 54+53', 'carrier':'NS', 'notes':''},
			{'yard':'Duryea yard 10+01', 'carrier':'RBMN', 'notes':''},
		]}, {'city':'Harrisburg area:', 'yards': [
			{'yard':'Enola YD (79)', 'carrier':'NS', 'notes':''},
			{'yard':'Harrisburg YD', 'carrier':'NS', 'notes':''},
			{'yard':'Rutherford YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Langhorne', 'yards': [	{'yard':'Woodbourne YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Reading', 'yards': [	{'yard':'Spring Street YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Philadelphia', 'yards': [	{'yard':'South Philadelphia YD*', 'carrier':'', 'notes':''},
			{'yard':'West Philadelphia YD*', 'carrier':'', 'notes':''},
		]}, {'city':'Scranton', 'yards': [	{'yard':'Scranton YD', 'carrier':'DL/Steamtown', 'notes':''},
		]}, {'city':'Taylor', 'yards': [	{'yard':'Taylor YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'York', 'yards': [	{'yard':'Windsor Street YD', 'carrier':'NS', 'notes':''},
		]}
	]},
	{'state':'Quebec', 'cities': [
		{'city':'Montreal', 'yards': [
			{'yard':'Taschereau YD', 'carrier':'CN', 'notes':'IM, MSH; former Hump YD'},
			{'yard':'St. Luc YD', 'carrier':'CP', 'notes':'MSH, Expressway'},
			{'yard':'Lachine', 'carrier':'CP', 'notes':'IM'},
			{'yard':'Hochelaga YD', 'carrier':'CP', 'notes':'IM'},
			{'yard':'Turcot', 'carrier':'CN', 'notes':'IM'},
			{'yard':'Riviére-des-Prairies', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Southwark YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Farnham', 'yards': [	{'yard':'Farnham YD', 'carrier':'MMA', 'notes':'MSH'},
		]}, {'city':'Trois-Rivieres', 'yards': [	{'yard':'Trois-Rivieres YD', 'carrier':'CFQG', 'notes':'MSH'},
		]}, {'city':'Saint-Georges Mauricie', 'yards': [
			{'yard':'Garneau YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Quebec City', 'yards': [
			{'yard':'Joffre YD', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Sainte-Foy', 'carrier':'CN', 'notes':'MSH'},
			{'yard':'Henri-IV YD', 'carrier':'CFQG', 'notes':'MSH'},
			{'yard':'Limoilou', 'carrier':'CN/CFC', 'notes':'MSH'},
		]}, {'city':'Mont-Joli', 'yards': [	{'yard':'Mont-Joli', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'La Tuque', 'yards': [
			{'yard':'Fitzpatrick YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Richmond', 'yards': [	{'yard':'Richmond YD', 'carrier':'CN/SLQ', 'notes':'MSH'},
		]}
	]},
	{'state':'Rhode Island', 'cities': [
		{'city':'North Kingstown', 'yards': [	{'yard':'Davisville YD', 'carrier':'PW/Seaview', 'notes':''},
		]}, {'city':'Valley Falls', 'yards': [	{'yard':'Lonsdale YD', 'carrier':'PW', 'notes':''},
		]}
	]},
	{'state':'Saskatchewan', 'cities': [
		{'city':'Moose Jaw', 'yards': [
			{'yard':'Moose Jaw YD', 'carrier':'CP', 'notes':'MSH'},
		]}, {'city':'Regina', 'yards': [
			{'yard':'Regina YD', 'carrier':'CP', 'notes':'IM, MSH'},
			{'yard':'Warell YD', 'carrier':'CN', 'notes':'MSH'},
		]}, {'city':'Saskatoon', 'yards': [
			{'yard':'Chappell YD', 'carrier':'CN', 'notes':'IM, MSH'},
			{'yard':'Sutherland YD', 'carrier':'CP', 'notes':'IM, MSH'},
		]}, {'city':'Melville', 'yards': [
			{'yard':'Melville YD', 'carrier':'CN', 'notes':'MSH'},
		]}
	]},
	{'state':'Tennessee', 'cities': [
		{'city':'Chattanooga', 'yards': [	{'yard':'DeButts YD (60)', 'carrier':'NS', 'notes':''},
			{'yard':'Wauhatchie YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Knoxville', 'yards': [	{'yard':'John Sevier YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Memphis', 'yards': [	{'yard':'Harrison', 'carrier':'CN', 'notes':''},
			{'yard':'Leewood YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Tennessee YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Nashville', 'yards': [	{'yard':'Radnor YD', 'carrier':'CSXT', 'notes':''},
			{'yard':'Kayne Ave. YD', 'carrier':'CSXT', 'notes':''},
		]}
	]},
	{'state':'Texas', 'cities': [
		{'city':'Arlington', 'yards': [	{'yard':'Arlington YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Beaumont', 'yards': [	{'yard':'Beaumont YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Fort Worth', 'yards': [	{'yard':'Davidson YD', 'carrier':'UP', 'notes':''},
			{'yard':'Tower 55', 'carrier':'UP/BNSF', 'notes':''},
		]}, {'city':'Garland', 'yards': [	{'yard':'Garland YD', 'carrier':'KCS', 'notes':''},
		]}, {'city':'Houston', 'yards': [	{'yard':'Englewood YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Kendleton', 'yards': [	{'yard':'Kendleton YD', 'carrier':'KCS', 'notes':''},
		]}, {'city':'Mesquite', 'yards': [	{'yard':'Mesquite Intermodal Facility', 'carrier':'UP', 'notes':''},
		]}, {'city':'Slaton', 'yards': [	{'yard':'Slaton YD', 'carrier':'BNSF/South Plains Lamesa', 'notes':''},
		]}
	]},
	{'state':'Utah', 'cities': [
		{'city':'Helper', 'yards': [	{'yard':'Helper YD', 'carrier':'UP/Utah', 'notes':''},
		]}, {'city':'Midvale', 'yards': [	{'yard':'Midvale YD', 'carrier':'BNSF/Utah Southern', 'notes':''},
		]}, {'city':'Provo', 'yards': [	{'yard':'Provo YD', 'carrier':'UP/BNSF/Utah', 'notes':''},
		]}, {'city':'Ogden', 'yards': [	{'yard':'Riverdale YD', 'carrier':'UP/Utah Central', 'notes':''},
		]}, {'city':'Salt Lake City', 'yards': [	{'yard':'North YD', 'carrier':'UP', 'notes':''},
			{'yard':'Roper YD', 'carrier':'UP', 'notes':''},
		]}
	]},
	{'state':'Virginia', 'cities': [
		{'city':'Alexandria:', 'yards': [	{'yard':'Potomac YD*', 'carrier':'RF&P', 'notes':''},
		]}, {'city':'Norfolk', 'yards': [	{'yard':'Lamberts Point YD', 'carrier':'NS', 'notes':'coal'},
		]}, {'city':'Chesapeake', 'yards': [	{'yard':'Portlock YD', 'carrier':'NS', 'notes':'IM, GM'},
			{'yard':'Berkley YD', 'carrier':'Norfolk & Portsmouth Belt Line / CSXT', 'notes':'GM'},
		]}, {'city':'Virginia Beach', 'yards': [	{'yard':'Little Creek YD', 'carrier':'Buckingham Branch', 'notes':'GM'},
		]}, {'city':'Richmond', 'yards': [	{'yard':'Fulton YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Roanoka', 'yards': [	{'yard':'Virginia Roanoke Terminal', 'carrier':'NS', 'notes':'coal GM'},
		]}
	]},
	{'state':'Washington', 'cities': [
		{'city':'Auburn', 'yards': [	{'yard':'Auburn YD*', 'carrier':'', 'notes':''},
		]}, {'city':'Cheney', 'yards': [	{'yard':'Cheney YD', 'carrier':'BNSF/WER', 'notes':''},
		]}, {'city':'Coulee City', 'yards': [	{'yard':'Coulee City YD', 'carrier':'WER', 'notes':''},
		]}, {'city':'Everett', 'yards': [	{'yard':'Delta YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Fife', 'yards': [	{'yard':'Fife YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Davenport', 'yards': [	{'yard':'Davenport YD', 'carrier':'WER', 'notes':''},
		]}, {'city':'Kettle Falls', 'yards': [	{'yard':'Kettle Falls YD', 'carrier':'STPP', 'notes':''},
		]}, {'city':'Longview', 'yards': [
			{'yard':'Longview Junction', 'carrier':'LVSW', 'notes':''},
			{'yard':'Longview', 'carrier':'LVSW', 'notes':''},
		]}, {'city':'Marshal', 'yards': [	{'yard':'Marshal', 'carrier':'UP/BNSF/SSPR', 'notes':''},
		]}, {'city':'Newport', 'yards': [	{'yard':'Newport YD', 'carrier':'POVA', 'notes':''},
		]}, {'city':'Pasco', 'yards': [
			{'yard':'Pasco YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Lampson YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Reardan', 'yards': [	{'yard':'Reardan YD', 'carrier':'WER', 'notes':''},
		]}, {'city':'Seattle', 'yards': [
			{'yard':'Argo YD', 'carrier':'UP', 'notes':''},
			{'yard':'Balmer YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'South Seattle', 'carrier':'BNSF', 'notes':''},
			{'yard':'Stacy YD/Seattle Intermodal Gateway', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Spokane', 'yards': [
			{'yard':'East Spokane YD', 'carrier':'UP', 'notes':''},
			{'yard':'Erie Street YD', 'carrier':'BNSF/UP', 'notes':''},
			{'yard':'HillYD YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'YDley YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Tacoma', 'yards': [	{'yard':'Tide Flats YD', 'carrier':'TMRW', 'notes':''},
			{'yard':'Tacoma YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Usk', 'yards': [	{'yard':'Usk YD & Shops', 'carrier':'POVA', 'notes':''},
		]}, {'city':'Vancouver', 'yards': [	{'yard':'Vancouver YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Warden', 'yards': [	{'yard':'Warden YD', 'carrier':'BNSF', 'notes':''},
		]}, {'city':'Wishram', 'yards': [	{'yard':'Wishram YD', 'carrier':'BNSF', 'notes':''},
		]}
	]},
	{'state':'West Virginia', 'cities': [
		{'city':'Bluefield', 'yards': [	{'yard':'Bluefield YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Grafton', 'yards': [	{'yard':'Grafton YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Keyser', 'yards': [	{'yard':'Keyser YD', 'carrier':'CSXT', 'notes':''},
		]}, {'city':'Prichard', 'yards': [	{'yard':'Prichard YD', 'carrier':'NS', 'notes':''},
		]}, {'city':'Williamson', 'yards': [	{'yard':'Williamson YD', 'carrier':'NS', 'notes':''},
		]}
	]},
	{'state':'Wisconsin', 'cities': [
		{'city':'Altoona', 'yards': [	{'yard':'Altoona YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Butler', 'yards': [	{'yard':'Butler YD', 'carrier':'UP', 'notes':''},
		]}, {'city':'Fond du Lac', 'yards': [	{'yard':'Shops YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Green Bay', 'yards': [	{'yard':'Green Bay YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Janesville', 'yards': [	{'yard':'Janesville YD', 'carrier':'WSOR', 'notes':''},
		]}, {'city':'La Crosse', 'yards': [	{'yard':'La Crosse YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'La Crosse YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Madison', 'yards': [	{'yard':'Madison YD', 'carrier':'WSOR', 'notes':''},
		]}, {'city':'Milwaukee', 'yards': [	{'yard':'Mitchell Street YD', 'carrier':'', 'notes':''},
			{'yard':'North Milwaukee YD', 'carrier':'WSOR', 'notes':''},
			{'yard':'Muskego YD', 'carrier':'CP', 'notes':''},
			{'yard':'National Avenue YD', 'carrier':'', 'notes':''},
		]}, {'city':'Neenah', 'yards': [	{'yard':'Neenah YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Portage', 'yards': [	{'yard':'Portage YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Stevens Point', 'yards': [	{'yard':'Stevens Point YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Superior', 'yards': [	{'yard':'28th Street YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Allouez YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Itasca YD', 'carrier':'UP', 'notes':''},
			{'yard':'Old Town YD', 'carrier':'BNSF', 'notes':''},
			{'yard':'Pokegama YD', 'carrier':'CN', 'notes':''},
			{'yard':'Stinson YD', 'carrier':'CP', 'notes':''},
		]}, {'city':'Wausau', 'yards': [	{'yard':'Wausau YD', 'carrier':'CN', 'notes':''},
		]}, {'city':'Wisconsin Rapids', 'yards': [	{'yard':'Wisconsin Rapids YD', 'carrier':'CN', 'notes':''},
		]}
	]}
]
