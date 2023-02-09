#!/bin/sh

if [ $# -lt 1 ]
then
	echo "Arguments incorrects"
	echo "Utilisations possibles :\n    sh isolate_call.sh init [options à passer à l'appel isolate --init]\n    sh isolate_call.sh move [chemin du répertoire isolé] [liste des fichiers/dossiers à déplacer]\n    sh isolate_call.sh run [options de l'appel à isolate --run] --run [chemin (absolu si hors du dossier isolé) du programme à exécuter + arguments du programme]\n    sh isolate_call.sh get_results [même arguments qu'une commande cp]\n    sh isolate_call.sh clean [options à passer à l'appel isolate --cleanup]"
else
	case $1 in
		init)
		# options du init à passer en argument
			shift 1
			echo $(isolate $* --init)
			;;

		move)
		# version légèrement assistée (un peu plus restrictive)
		# 	chemin jusqu'à l'environement isolé à passer en 1er argument,
		#	puis liste des répertoires à déplacer dans l'environement
			shift 1 
			
			REP="$1/box"
			shift 1
			echo $(cp -r $* $REP)
			;;

		# alternative plus simple
		# 	argument d'un appel cp passés en arguments
#			shift 1
#			sudo cp $*
#			;;

		run)
		# options du run à passer en arguments,
		# 	puis --run (pour éviter de parser les arguments...)
		#	puis programme à exécuter avec ses arguments
			shift 1
			echo $(isolate $*)
			;;

		get_results)
		# version légèrement assistée (un peu plus restrictive : les fichiers de sortie à récupérer doivent être placés dans un dossier res à la racine de l'environement isolé)
		# 	chemin jusqu'à l'environement isolé à passer en 1er argument,
		# 	puis chemin du dossier où sera stocker le dossier res
#			shift 1
#			REP="$1/box/res"
#			shift 1
#			cp $REP $*
#			;;
			
		# alternative plus simple
		#	argument d'un appel cp passés en arguments
			shift 1
			echo $(cp $*)
			;;

		clean)
		# options du cleanup à passer en argument
			shift 1
			echo $(isolate $* --cleanup)
			;;
			
		*)
			echo "Commande erronée"
			echo "Utilisations possibles :\n    sh isolate_call.sh init [options à passer à l'appel isolate --init]\n    sh isolate_call.sh move [chemin du répertoire isolé] [liste des fichiers/dossiers à déplacer]\n    sh isolate_call.sh run [options de l'appel à isolate --run] --run [chemin (absolu si hors du dossier isolé) du programme à exécuter + arguments du programme]\n    sh isolate_call.sh get_results [même arguments qu'une commande cp]\n    sh isolate_call.sh clean [options à passer à l'appel isolate --cleanup]"

	esac
fi
