from .logger import Logger

class FirebaseHandler:
    def __init__(self, credential_path, collection_name):
        # Firebase initialization
        ...

    @staticmethod
    def validate_document(data, robot_type, is_requested):
        required_keys = ["robot", "state", "datetime"]
        if not all(key in data for key in required_keys):
            Logger().warning("Skipping invalid document: Missing required keys")
            return None
        if data.get("robot") != robot_type or data.get("state") != is_requested:
            return None
        return data

    def fetch_and_sort_data(self, robot_type, is_requested):
        try:
            docs = self.db.collection(self.collection_name).stream()
            filtered_data = []

            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                validated_data = self.validate_document(data, robot_type, is_requested)
                if validated_data:
                    filtered_data.append(validated_data)

            if not filtered_data:
                Logger().info("No valid data found matching the criteria.")
                return []

            filtered_data.sort(key=lambda x: x["datetime"])
            return filtered_data

        except Exception as e:
            Logger().error(f"Error fetching data from Firebase: {e}")
            return []
