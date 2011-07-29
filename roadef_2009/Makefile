all:
	mkdir -p IFAM
	python ./scripts/to_IFAM.py ./raw/A01_6088570/ > IFAM/A_01_IFAM.json
	#same as A_01: A_02, A_03, A_04, XA_01
	python ./scripts/to_IFAM.py ./raw/A05_6088570/ > IFAM/A_05_IFAM.json
	#same as A_05: XA02
	python ./scripts/to_IFAM.py ./raw/A06_6088590/ > IFAM/A_06_IFAM.json
	#same as A_06: A_07, A_08, A_09, XA03
	python ./scripts/to_IFAM.py ./raw/A10_6088590/ > IFAM/A_10_IFAM.json
	#same as A_10: XA04
	python ./scripts/to_IFAM.py ./raw/B_01/        > IFAM/B_01_IFAM.json
	#same as B_01: B_02, B_03, B_04, B_05, XB01, XB02
	python ./scripts/to_IFAM.py ./raw/B_06/        > IFAM/B_06_IFAM.json
	#same as B_06: B07, B_08, B_09, B_10, XB03, XB04
	python ./scripts/to_IFAM.py ./raw/X01_DATA/    > IFAM/X_01_IFAM.json
	#same as X_01: X_02
	python ./scripts/to_IFAM.py ./raw/X03_DATA/    > IFAM/X_03_IFAM.json
	#same as X_03: X_04

clean:
	rm -rf IFAM
