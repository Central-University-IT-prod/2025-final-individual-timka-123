from django.conf import settings
from yandex_cloud_ml_sdk import YCloudML


class YaGpt:
    def __init__(self, folder_id: str, auth: str):
        self.sdk = YCloudML(
            folder_id=folder_id,
            auth=auth
        )
        self.mod_model = self.sdk.models.text_classifiers("yandexgpt")
        self.mod_model = self.mod_model.configure(
            task_description=settings.MODERATION_START_PROMPT,
            labels=["НЕТ", "ДА", "НЕ ЗНАЮ"]
        )

        self.text_model = self.sdk.models.completions("yandexgpt")
        self.text_model = self.text_model.configure(
            temperature=0.3
        )
        self.data = [{
            "role": "system",
            "text": """Представь себе, что ты креативщик в рекламном агентстве и тебе нужно придумывать описания рекламных объявлений по их названию. Они должны захватывать внимание и быть яркими и сочными. ПИШИ ОДНИМ АБЗАЦЕМ
Длина итогового текста МИНИМУМ 150 СИМВОЛОВ
Если название нарушает правила Яндекс Директа, то пиши "НЕЛЬЗЯ""",
        }]

    def check_text(self, text: str) -> bool:
        result = self.mod_model.run(text)
        best_pred = sorted(
            result.predictions, key=lambda item: item.confidence, reverse=True
        )[0]
        return best_pred.label == "ДА"
    
    def generate_description(self, title: str) -> str:
        data = self.data
        data.append({
            "role": "user",
            "text": title
        })
        result = self.text_model.run(data)
        return result.alternatives[0].text
