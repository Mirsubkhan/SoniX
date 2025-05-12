from infrastructure.telegram.bot import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())

# TODO: Исправить баг с динамической транскрибацией (нашёл баг, но не исправил ещё)
# TODO: Добавить удаление сообщений после нажатия на кнопки (не выполнено)
# TODO: Добавить удаление файлов после операций (не выполнено)
