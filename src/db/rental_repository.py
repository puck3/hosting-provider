from datetime import datetime, timedelta
from psycopg2.extras import RealDictCursor

from src.db.base import BaseRepository
from src.db.server_repository import ServerRepository
from src.models.plan import BillingPeriod
from src.models.rental import Rental, UserData
from src.models.server import Server
from src.models.user import User
from src.services.repositories_abc import RentalRepositoryABC


class RentalRepository(BaseRepository, RentalRepositoryABC):
    def create_rental(
        self, user: User, server: Server, price: float, billing_period: BillingPeriod
    ) -> Rental:
        query = """
            INSERT INTO rentals (
                user_id, server_id, price, billing_period, start_at, end_at, update_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING rental_id;
        """
        start_at = end_at = datetime.now()
        match billing_period:
            case BillingPeriod.hourly:
                end_at += timedelta(hours=1)
            case BillingPeriod.daily:
                end_at += timedelta(days=1)
            case BillingPeriod.monthly:
                end_at += timedelta(days=30)

        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        user.user_id,
                        server.server_id,
                        price,
                        billing_period,
                        start_at,
                        end_at,
                        start_at,
                    ),
                )
                rental_id = cursor.fetchone()[0]
            conn.commit()

        user_data = UserData(user_id=user.user_id, login=user.login, email=user.email)
        rental = Rental(
            rental_id=rental_id,
            user=user_data,
            server=server,
            price=price,
            billing_period=billing_period,
            start_at=start_at,
            end_at=end_at,
            update_at=start_at,
        )
        return rental

    def save_rental(self, rental: Rental) -> None:
        query = """
            UPDATE rentals
            SET server_id = %s, price = %s, billing_period = %s, end_at = %s
            WHERE rental_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        rental.server.server_id,
                        rental.price,
                        rental.billing_period,
                        rental.end_at,
                        rental.rental_id,
                    ),
                )
            conn.commit()

    @staticmethod
    def get_rental_from_record(record: dict | None) -> Rental | None:
        if record is None:
            return None
        else:
            rental_data = {
                key: value
                for key, value in record.items()
                if key in Rental.model_fields.keys()
            }
            user_data = {
                key: value
                for key, value in record.items()
                if key in UserData.model_fields.keys()
            }
            rental_data["user"] = UserData(**user_data)
            rental_data["server"] = ServerRepository.get_server_from_record(record)
            return Rental(**rental_data)

    def get_rental_by_id(self, rental_id: int) -> Rental | None:
        query = """
            SELECT
                r.rental_id,
                r.price,
                r.billing_period,
                r.start_at,
                r.end_at,
                r.update_at,
                u.user_id,
                u.email,
                u.login,
                s.server_id,
                s.status,
                s.operating_system,
                d.datacenter_id,
                d.datacenter_name,
                d.country,
                d.city,
                h.hardware_id,
                h.cpu_id,
                h.cpu_name,
                h.cpu_vendor,
                h.cores,
                h.frequency,
                h.cpus_count,
                h.gpu_id,
                h.gpu_name,
                h.gpu_vendor,
                h.vram_type,
                h.vram_gb,
                h.gpus_count,
                h.storage_tb,
                h.ram_gb,
                h.bandwidth_gbps
            FROM rentals r
            LEFT JOIN users u USING (user_id)
            LEFT JOIN servers s USING (server_id)
            LEFT JOIN datacenters d USING (datacenter_id)
            LEFT JOIN extended_hardwares h USING (hardware_id) 
            WHERE r.rental_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (rental_id,))
                result = cursor.fetchone()

        return self.get_rental_from_record(result)

    def get_rentals(self) -> list[Rental]:
        query = """
            SELECT
                r.rental_id,
                r.price,
                r.billing_period,
                r.start_at,
                r.end_at,
                r.update_at,
                u.user_id,
                u.email,
                u.login,
                s.server_id,
                s.status,
                s.operating_system,
                d.datacenter_id,
                d.datacenter_name,
                d.country,
                d.city,
                h.hardware_id,
                h.cpu_id,
                h.cpu_name,
                h.cpu_vendor,
                h.cores,
                h.frequency,
                h.cpus_count,
                h.gpu_id,
                h.gpu_name,
                h.gpu_vendor,
                h.vram_type,
                h.vram_gb,
                h.gpus_count,
                h.storage_tb,
                h.ram_gb,
                h.bandwidth_gbps
            FROM rentals r
            LEFT JOIN users u USING (user_id)
            LEFT JOIN servers s USING (server_id)
            LEFT JOIN datacenters d USING (datacenter_id)
            LEFT JOIN extended_hardwares h USING (hardware_id) 
            ORDER BY r.rental_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [self.get_rental_from_record(record) for record in result]

    def get_rentals_by_user(self, user_id: int) -> list[Rental]:
        query = """
            SELECT
                r.rental_id,
                r.price,
                r.billing_period,
                r.start_at,
                r.end_at,
                r.update_at,
                u.user_id,
                u.email,
                u.login,
                s.server_id,
                s.status,
                s.operating_system,
                d.datacenter_id,
                d.datacenter_name,
                d.country,
                d.city,
                h.hardware_id,
                h.cpu_id,
                h.cpu_name,
                h.cpu_vendor,
                h.cores,
                h.frequency,
                h.cpus_count,
                h.gpu_id,
                h.gpu_name,
                h.gpu_vendor,
                h.vram_type,
                h.vram_gb,
                h.gpus_count,
                h.storage_tb,
                h.ram_gb,
                h.bandwidth_gbps
            FROM rentals r
            LEFT JOIN users u USING (user_id)
            LEFT JOIN servers s USING (server_id)
            LEFT JOIN datacenters d USING (datacenter_id)
            LEFT JOIN extended_hardwares h USING (hardware_id) 
            WHERE user_id = %s
            ORDER BY r.rental_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchall()

        return [self.get_rental_from_record(record) for record in result]
