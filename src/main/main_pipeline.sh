#verifier que les variables sont bien definis
vars="username password mail matiere gitlabArbre repository_path"
for element in $vars
do
  if test "$(eval echo \$$element)" = ""; then
    echo "variable environmentale $element is not defined, exiting ..."
    exit 0
  fi
done


#create variables json from environement variables
envsubst < src/variables_template.json > src/variables.json

if test "$CI_PIPELINE_SOURCE" = "trigger"; then
    # Récupérer la liste des fichiers modifiés
    curl --header "PRIVATE-TOKEN: $password" "https://gitlab.com/api/v4/projects/$PROJECT_SOURCE_ID/repository/commits/$COMMIT_SOURCE_SHA/diff" > response_diff.txt
    curl --header "PRIVATE-TOKEN: $password" "https://gitlab.com/api/v4/projects/$PROJECT_SOURCE_ID/repository/commits/$COMMIT_SOURCE_SHA" > response_project.txt

    cat response_diff.txt
    cat response_project.txt

    project_source_url=$(cat response_project.txt | jq -r '.web_url')
    # Extraire la liste des fichiers modifiés de la réponse JSON
    modified_files=$(cat response_diff.txt | jq -r '.[].new_path')
    cat response_project.txt | jq -r '.message' > commit_desc.txt

    if cat commit_desc.txt | grep -q 'automatique'; then
        echo "Le commit etait automatique abondan."
        exit 0 
    else
        args_EOD=$(python3 src/utils/get_args_EOD.py $project_source_url $modified_files)
        echo "Lancer evaluateOnDemand $args_EOD"    
        sh feat3p evaluateOnDemand $args_EOD
    fi

    # Afficher la liste des fichiers modifiés
    echo "project source url :"
    echo $project_source_url
    echo "Fichiers modifiés :"
    echo $modified_files
else
    if test "$type_evaluate" = "single"; then
        echo "lancer evaluate $args"
        sh feat3p evaluate $args
    else
        if test "$type_evaluate" = "all"; then 
            echo "lancer evaluateAll $args"
            sh feat3p evaluateAll $args
        else
            echo "varible type_evaluate not provided, exiting ..."
        fi
    fi
fi
