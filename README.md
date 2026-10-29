# Навыки проекта «Заря»

Публичные версии локальных навыков Codex. Обновлено 29 октября 2026 года. [Каталог и статус готовности](CATALOG.md).

| Навык | Назначение |
|---|---|
| [mango-staff-mobile-setup](skills/mango-staff-mobile-setup/SKILL.md) | Мобильные номера Mango, схемы, АОН и порученные тесты |
| [zarya-crm-semantic-layer](skills/zarya-crm-semantic-layer/SKILL.md) | Чтение Озера и интерпретация CRM-показателей |
| [zarya-unrecognized-cities](skills/zarya-unrecognized-cities/SKILL.md) | Только новые незаполненные привязки городов в исходном порядке |
| [zarya-skorozvon-trunks](skills/zarya-skorozvon-trunks/SKILL.md) | Контроль нагрузки и порученная ротация транков Скорозвона |
| [zarya-chatapp-campaigns](skills/zarya-chatapp-campaigns/SKILL.md) | Подготовка и порученные рассылки ChatApp |
| [zarya-campaign-results](skills/zarya-campaign-results/SKILL.md) | История и сравнение результатов рассылок |
| [zarya-call-reconciliation](skills/zarya-call-reconciliation/SKILL.md) | Сопоставление попыток Mango, Скорозвона и МТС |
| [zarya-callcity-testing](skills/zarya-callcity-testing/SKILL.md) | Совместные тесты Talker/CallCity, контроль линии и сохранности исходящего |
| [zarya-crm-incidents](skills/zarya-crm-incidents/SKILL.md) | Хронология повторных лидов и проверка причин |
| [zarya-pulse-development](skills/zarya-pulse-development/SKILL.md) | Разделы Пульса, расчёты и права пользователей |
| [zarya-data-freshness](skills/zarya-data-freshness/SKILL.md) | Диагностика свежести, покрытия и качества аналитики |
| [zarya-bp-audit](skills/zarya-bp-audit/SKILL.md) | Аудит конфигурации БП и доказательств исполнения |
| [zarya-telephony-city-pools](skills/zarya-telephony-city-pools/SKILL.md) | Сверка поставок, каталогов и городских пулов номеров |
| [zarya-admin24-integration](skills/zarya-admin24-integration/SKILL.md) | Разработка связи автора, заявки и уведомлений; backend не включён |
| [zarya-xiaomi-cameras](skills/zarya-xiaomi-cameras/SKILL.md) | Доступность камер Xiaomi, версии, порученное OTA и отчёты по городам |
| [mango-staff-mobile-online](skills/mango-staff-mobile-online/SKILL.md) | Подготовительная онлайн-версия; рабочего облачного подключения и записи нет |

| [zarya-client-questionnaire](skills/zarya-client-questionnaire/SKILL.md) | Логика Excel-анкеты КЦ, расхождения и подготовка переноса в Битрикс24 |

## Установка

Скопируйте нужные папки из skills в ~/.codex/skills. Для новых аналитических навыков и разработки Пульса установите также zarya-crm-semantic-layer. Его публичная версия содержит методику; производственная карта полей и подключения задаются локально.

## Границы публичной версии

Навыки не включают доступы, серверы инструментов, исходники Пульса, рабочие клиенты рассылки и Exolve, прототип и backend Админ24, прототип и backend Админ24, частные чаты или данные клиентов. Настройте разрешённые подключения отдельно и проверьте текущие контракты сервисов. Отсутствующий адаптер нельзя считать установленным по одной ссылке на него.

Озеро строго только для чтения. Наличие навыка не разрешает отправку сообщений, звонки, смену назначений, push или deploy: действия определяются поручением пользователя. Автоматический выбор навыка включён; он не запускает операции самостоятельно.

Внутренние адреса, пути к доступам и персональные примеры исключены. Локальные оригиналы сохранены отдельно.

## Проверка

У навыков проверены структура, ссылки и метаданные. Новые и обновлённые локальные навыки проходят также проверку рабочих сценариев; это не тест живых интеграций.

В mango-staff-mobile-setup/scripts есть офлайн-валидатор плана и тесты. assets/crmcalls-test.wav — синтезированная тестовая фраза; звонить с ней разрешено только по прямому поручению. Подготовительный mango-staff-mobile-online не становится работающей интеграцией от установки папки.
