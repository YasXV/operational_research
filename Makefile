# Variables
PYTHON = python
VENV = .venv
VENV_BIN = $(VENV)\Scripts

.PHONY: init install test clean

#initialiser l'environnement virtuel
init:
	if exist $(VENV) ( \
		echo "L'environnement virtuel $(VENV) existe déjà." \
	) else ( \
		echo "Création de l'environnement virtuel..." && \
		$(PYTHON) -m venv $(VENV) && \
		$(VENV_BIN)\python -m pip install --upgrade pip && \
		
	)


# Installer les dépendances
install:
	$(VENV_BIN)\pip install -e .
	$(VENV_BIN)\pip install -r requirements.txt \

# Lancer les tests
test:
	$(VENV_BIN)\pytest tests

# Nettoyer les fichiers inutiles
clean:
	if exist $(VENV) ( \
		rmdir /S /Q $(VENV) \
	) 
	del /F /Q *.pyc
	del /F /Q -Recurse __pycache__
