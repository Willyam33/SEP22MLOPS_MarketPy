error_messages = {
    'NOT_IN_RANGE': "Au moins un paramètre n est pas dans une fourchette acceptable !", 
    'MODEL_NOT_FOUND': "Le modèle n est pas disponible, contactez votre administrateur !",
    'NO_MODEL_IN_PRODUCTION': "Pas de modèle disponible en production !",
    'USER_UNKNOWN': "L utilisateur n existe pas !",
    'NOT_ADMIN': "L utilisateur n est pas administrateur !",
    'BAD_PASSWORD': "Le mot de passe est incorrect !",
    'ERREUR_A_DEFINIR': "ERREUR A DEFINIR !",
    'USER_ALREADY_EXISTS' : " existe déjà !", # to prefix by user
    'MODEL_ALREADY_IN_BASE' : " est déjà enregistré et disponible en base !", # to prefix by model
    'MODEL_UNKNOWN' : " n existe pas en base !",
    'DATABASE_ERROR' : "Erreur d accès à la base de données",
    'DATABASE_SELECT_ERROR' : "Erreur d accès en select à la base de données",
    'DATABASE_CREATION_ERROR' : "Erreur de création de la base de données",
    'DATABASE_DROP_ERROR' : "Erreur de suppression de la base de données",
    'DATABASE_INSERT_ERROR' : "Erreur d'insertion en base de données",
    'DATABASE_UPDATE_ERROR' : "Erreur de mise à jour base de données",
    'DATABASE_DELETE_ERROR' : "Erreur de suppression dans la base de données",
    'DATABASE_INCONSISTENCY' : "Base de données inconsistante",
    'UNABLE_TO_MANAGE_PRODUCTION_MODELS' : "Impossible de gérer le modèle de production",
    'UNABLE_TO_SAVE_DATASET_METADATA' : "Impossible de sauvegarder les metadonnées du dataseset. L ingestion peut être relancée manuellement ou automatiquement à la prochaine itération programmée.",
    'UNABLE_TO_LOAD_PRODUCTION_PIPELINE_FILE' : "Impossible de charger le fichier contenant le pipeline de production",
    'UNABLE_TO_SAVE_PRODUCTION_SCORING_ON_NEW_DATASET' : "Impossible de sauvegarder le score du modèle de production sur un nouveau dataset",
    'UNABLE_TO_DELETE_USER': " ne peut être supprimé !", # to prefix by user
    'UNABLE_TO_DELETE_MODEL': " ne peut être supprimé !", # to prefix by model
    'UNABLE_TO_ADD_USER': " ne peut être ajouté.e !", # to prefix by user
    'UNABLE_TO_ADD_MODEL': " ne peut être ajouté !", # to prefix by user
    'NO_RESULT' : "Aucun résultat"
}

warning_messages = {
    'NO_MODEL_IN_PRODUCTION': "Pas de modèle disponible en production !",
    'NO_PREDICTION_FOR_USER': "Aucune prédiction n a été trouvée (et probablement aucune n a été effectuée) pour ", # to suffix by user
    'NO_PREDICTION': "Aucune prédiction n a été trouvée (et probablement aucune n a été effectuée) !",
    'INVALID_DATASET' : "Le dataset est invalide. Aucun entrainement, ni aucun scoring ne pourra être effectué sur celui-ci."
}

success_messages = {
    'NEW_MODEL_IN_PRODUCTION': "Un nouvau modèle est disponible en production !",
    'PRODUCTION_SCORING_UPDATED': "Le score du modèle de production a été mis à jour sur la base du nouveau dataset !",
    'USER_DELETED' : " a été supprimé.e !", # to prefix by user
    'MODEL_DELETED' : " a été supprimé !", # to prefix by user
    'USER_ADDED' : " a été ajouté.e !", # to prefix by user
    'MODEL_ADDED' : " a été ajouté !" # to prefix by user
}




 