class _:
    # Subscriptions
    subscription_approved = "Подписка на {topic} выполнена"
    command_from_topic = 'Команда из топика {topic}: {command}'


class TOPICS:
    # subscription topics
    response_sub = 'devices/{device_id}/response'
    new_device_sub = 'devices/new_device'

    # publish topics
    control_topic_pub = 'devices/{device_id}/control'
