all: IFAM FAM MDFAM

IFAM:
	mkdir -p IFAM
	python ./scripts/to_IFAM.py ./raw/A01_6088570/ > IFAM/A_01_IFAM.json
	python ./scripts/to_IFAM.py ./raw/A05_6088570/ > IFAM/A_05_IFAM.json
	python ./scripts/to_IFAM.py ./raw/A06_6088590/ > IFAM/A_06_IFAM.json
	python ./scripts/to_IFAM.py ./raw/A10_6088590/ > IFAM/A_10_IFAM.json
	python ./scripts/to_IFAM.py ./raw/B_01/        > IFAM/B_01_IFAM.json
	python ./scripts/to_IFAM.py ./raw/B_06/        > IFAM/B_06_IFAM.json
	python ./scripts/to_IFAM.py ./raw/X01_DATA/    > IFAM/X_01_IFAM.json
	python ./scripts/to_IFAM.py ./raw/X03_DATA/    > IFAM/X_03_IFAM.json

FAM: IFAM
	mkdir -p FAM
	python ./scripts/IFAM_to_FAM.py ./IFAM/A_01_IFAM.json > ./FAM/A_01_FAM.json
	python ./scripts/IFAM_to_FAM.py ./IFAM/A_05_IFAM.json > ./FAM/A_05_FAM.json
	python ./scripts/IFAM_to_FAM.py ./IFAM/A_06_IFAM.json > ./FAM/A_06_FAM.json
	python ./scripts/IFAM_to_FAM.py ./IFAM/A_10_IFAM.json > ./FAM/A_10_FAM.json
	python ./scripts/IFAM_to_FAM.py ./IFAM/B_01_IFAM.json > ./FAM/B_01_FAM.json
	python ./scripts/IFAM_to_FAM.py ./IFAM/B_06_IFAM.json > ./FAM/B_06_FAM.json
	python ./scripts/IFAM_to_FAM.py ./IFAM/X_01_IFAM.json > ./FAM/X_01_FAM.json
	python ./scripts/IFAM_to_FAM.py ./IFAM/X_03_IFAM.json > ./FAM/X_03_FAM.json

MDFAM: IFAM
	mkdir -p MDFAM
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/A_01_IFAM.json > ./MDFAM/A_01_MDFAM.json
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/A_05_IFAM.json > ./MDFAM/A_05_MDFAM.json
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/A_06_IFAM.json > ./MDFAM/A_06_MDFAM.json
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/A_10_IFAM.json > ./MDFAM/A_10_MDFAM.json
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/B_01_IFAM.json > ./MDFAM/B_01_MDFAM.json
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/B_06_IFAM.json > ./MDFAM/B_06_MDFAM.json
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/X_01_IFAM.json > ./MDFAM/X_01_MDFAM.json
	python ./scripts/IFAM_to_MDFAM.py ./IFAM/X_03_IFAM.json > ./MDFAM/X_03_MDFAM.json

clean:
	rm -rf IFAM FAM MDFAM
