import os
import sys
import django
from dotenv import load_dotenv
import traceback
from datetime import datetime

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "international_delivery.settings")
django.setup()

load_dotenv()

from delivery.tasks import ConsumerMQ, callback_mq

def main():
    consumer = ConsumerMQ()

    consumer.consume(callback_mq)
    consumer.start_consuming()
    
    # except Exception as exc:
    #     print(8)
    #     print(exc)
    # finally:
    #     print(3)
    #     consumer.stop_consuming()
    #     # traceback.print_exc()


if __name__ == '__main__':
    main()