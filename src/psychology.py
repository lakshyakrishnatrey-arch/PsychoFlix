class PsychologyEngine:

    def __init__(self):

        self.genre_to_emotion = {

            "Comedy": ["😊 Happy", "😌 Relaxed"],

            "Family": ["😌 Relaxed", "😊 Happy"],

            "Animation": ["😊 Happy", "😌 Relaxed"],

            "Adventure": ["💪 Motivated", "😊 Happy"],

            "Action": ["💪 Motivated", "😡 Angry"],

            "Drama": ["🤔 Reflective", "😤 Frustrated"],

            "Romance": ["❤️ Romantic"],

            "Fantasy": ["🌈 Escapism"],

            "Science Fiction": ["🤔 Curious", "🌈 Escapism"],

            "Mystery": ["🤔 Curious", "😤 Frustrated"],

            "Thriller": ["⚡ Excited", "😤 Frustrated"],

            "Crime": ["⚡ Excited", "😡 Angry"],

            "Horror": ["😱 Fear"],

            "Documentary": ["📚 Learning"],

            "History": ["📚 Learning"],

            "War": ["🤔 Reflective", "😡 Angry"],

            "Music": ["😊 Happy"],

            "Western": ["💪 Motivated", "😡 Angry"]
        }

    def emotions_from_genres(self, genres):

        emotions = []

        for genre in genres:

            emotions.extend(
                self.genre_to_emotion.get(genre, [])
            )

        return sorted(list(set(emotions)))