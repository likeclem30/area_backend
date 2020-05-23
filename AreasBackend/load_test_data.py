from areas_backend.app import create_app
from areas_backend.models import AreaModel


if __name__ == '__main__':
    application = create_app()
    application.app_context().push()

    # Create some test data
    test_data = [
        # username, timestamp, text
        ('bruce', "1962-05-11 09:53:41Z", "k1G", "Karu", "A2J"),
        ('bruce', "1962-05-11 09:58:23Z", "K2G", "Karu2", "A2J"),
        ('bruce', "1962-05-11 10:07:13Z", "K3G", "Karu3", "A2J"),
        ('stephen', "1963-06-11 19:53:41Z", "K4G", "Karu4", "A2J"),

    ]
    for username, timestamp, areacode, area, zonecode in test_data:
        area = AreaModel(username=username, areacode=areacode,
                         area=area, zonecode=zonecode, timestamp=timestamp)
        application.db.session.add(area)

    application.db.session.commit()
