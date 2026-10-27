# Проверенный контракт Mango для настройки сотрудников

Подтверждён 21.10.2026, перепроверять при изменении схемы API. Не является публичной гарантией неизменности интерфейса.

## Доступ

Авторизация: `https://auth.mango-office.ru/auth/vpbx`, JSON `username,password,app:"mlk",device_id:<fresh random>`. Разрешённый источник учётных данных в текущей среде указан в существующем рабочем подключении; не проси печатать пароль в чат. Секретные значения/токены в навык не включать.

Успех входа: `result=1000` и `auth_token`. Если нужен OTP/подтверждение - остановиться и предоставить пользователю авторизацию в UI, не обходить её.

GraphQL: `https://api-mvpbx.mango-office.ru/graphql/mvpbx`, JSON `query`/`variables`, заголовок `Authorization: Bearer …`. Не следовать редиректам с токеном, ограничить таймаут/ответ. Проверять GraphQL `errors`, затем прикладной `status`.

Через `account { products { id } }` проверь продукт. В исходной задаче продукт `<PRODUCT_ID>`; это контекст, не разрешение работать с ним без проверки текущего поручения.

Для неизвестных входных типов используй безопасную introspection `__type`, не пробные mutations. Не запрашивай `Member.password`, лишние персональные контакты или SIP-секреты.

## Чтение

```graphql
query($product: ID!) {
  incomingLines(product_id: $product) {
    number abonent_id profile_id number_desc number_title
    number_type active_fwd_schema_id
  }
  members(product_id: $product) {
    id name extension default_number_id subst_ani_abonent_id
    use_cc_numbers use_status role_id sip_access dial_algorithm
  }
  fwdSchemas(product_id: $product) { id name desc lines }
}
```

Проверь полноту результата. При необходимости используй `membersPaginate` с контрольными количествами. Для точного сопоставления можно читать `members(member_id: …)`/`members(search_text: …)` и `groups(group_id: …)`.

Дерево: `fwdSchemaItems(product_id:…,schema_id:…) {status details schema {schema_id ivr {…}}}`. Рекурсивные поля узла: `type action condition {type dtmf_key failed_count} attributes {target fwd_target_id fwd_number mbr_strategy timeout disable} items {…}`. Читай достаточную глубину, не считай обрезанное дерево полным.

Перед копированием более сложной схемы дополнительно прочитай `schedule`, приветствия, условия и все применённые атрибуты через introspection. Не копируй частичную проекцию дерева как полную настройку.

## Точечные mutations

Ниже контракты, а не автоматическое разрешение на выполнение.

### Подпись (до 40 символов)

```graphql
mutation($p: ID!, $n: ID!, $text: String!) {
  numberDescUpdate(product_id:$p, abonent_id:$n, description:$text) {
    status details
  }
}
```

При превышении лимита: `status=3100`, `Description too long! Max length - 40 symbols`. Согласованные инициалы используй целиком; не произвольное срезание строки.

### Создание отдельной схемы

`fwdSchemaAdd(product_id:ID!,schema_name:String,schema_desc:String,ivr:[InputFwdSchemaIVR]!) {status details schema {schema_id}}`

Проверенный простой последовательный IVR (ID подставить из живых объектов):

```json
[
  {"type":"PROCEDURE","items":[
    {"type":"ACTION","action":"DIAL","attributes":{
      "target":"MEMBER","fwd_target_id":123,"mbr_strategy":"DEF_NUMBER","timeout":20}},
    {"type":"ACTION","action":"DIAL","attributes":{
      "target":"MEMBER","fwd_target_id":456,"mbr_strategy":"DEF_NUMBER","timeout":20}},
    {"type":"ACTION","action":"DIAL","attributes":{
      "target":"ACD","fwd_target_id":789}}
  ]}
]
```

`DEF_NUMBER` вызывает номер сотрудника по умолчанию. Не выбирай его, если пользователь просил другой алгоритм/устройство. `BY_MEMBER` - другая стратегия, не менять молча. На финальной ACD сохраняй настройки утверждённой группы; не добавляй без поручения новое завершение/голосовую почту/ночной график.

После `status=1000` получи ID и прочитай полное созданное дерево; совпадение имени недостаточно. При неопределённом исходе создания сверяй каталог/журнал, не повторяй создание.

### Активация только на выбранной линии

`fwdSchemaActivate(schema_id:ID!,profile_id:ID!,product_id:ID!) {status details}`

После проверь `incomingLines.active_fwd_schema_id`. В каталоге старая схема теряет `abonent_id` выбранного номера, новая получает его. Связи других линий должны сохраниться.

Не использовать `fwdSchemaSettingsUpdate` для изменения общей схемы вместо создания отдельной.

### Исходящий АОН

```graphql
mutation($p: ID!, $m: ID!, $number: ID!) {
  memberUpdate(product_id:$p, member_id:$m,
    params:{subst_ani_abonent_id:$number}) {status details}
}
```

В `InputMemberUpdate` поле `subst_ani_abonent_id` описано как `Outgoing number`. Значение - **abonent_id линии**, не телефонная строка, не `profile_id`, не `default_number_id`.

Перед записью проверь `use_cc_numbers`; включённый выбор номеров контакт-центра требует отдельной оценки. Не отправляй пустые `numbers`, другие поля или полный объект сотрудника: это может изменить устройства/прочие настройки.

## Контроль результата

В журнал записывай статус до/после каждой записи и безопасный ответ, без токенов и паролей. Для read-back допустимы интервалы 0 / 0,5 / 1 / 2 / 4 / 8 секунд. Это повтор **чтения**, не mutation. Запись HTTP 200 без `status=1000` не успех.

При успешном конце убедись, что различия между исходным/конечным состояниями ровно запланированные. Не выдавай это за проверку телефонного звонка или фактического АОН на телефоне клиента.

## Пример выполненного сопоставления (исторический, не для повторного запуска)

21.10.2026 были созданы отдельные схемы `<SCHEMA_A>`, `<SCHEMA_B>`, `<SCHEMA_C>` для трёх тестовых сотрудников. Этот факт нужен для распознавания повторной задачи и проверки уже существующих схем, не для назначения этих ID новым сотрудникам.
