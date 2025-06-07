from psycopg2.extras import RealDictCursor

from app.db.base import BaseRepository
from app.db.hardware_repository import HardwareRepository
from app.models.hardware import Hardware
from app.models.plan import BillingPeriod, Plan
from app.services.repositories_abc import PlanRepositoryABC


class PlanRepository(BaseRepository, PlanRepositoryABC):
    def create_plan(
        self,
        hardware: Hardware,
        price: float,
        billing_period: BillingPeriod,
        plan_name: str,
        plan_description: str,
    ) -> Plan:
        query = """
            INSERT INTO plans (
                hardware_id, price, billing_period, plan_name 
            ) 
            VALUES (
                %s, %s, %s, %s
            )
            RETURNING plan_id;
        """
        hardware_id = hardware.hardware_id
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (hardware_id, price, billing_period, plan_name),
                )
                result = cursor.fetchone()
                conn.commit()

            if result is None:
                raise RuntimeError("Failed to create plan")

            plan_id = result[0]

        plan = Plan(
            plan_id=plan_id,
            hardware=hardware,
            price=price,
            billing_period=billing_period,
            plan_name=plan_name,
        )
        return plan

    def delete_plan(self, plan_id: int) -> None:
        query = """
            DELETE FROM plans
            WHERE plan_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (plan_id,))
            conn.commit()

    @staticmethod
    def get_plan_from_record(record: dict | None) -> Plan | None:
        if record is None:
            return None
        else:
            plan_data = {key: value for key, value in record.items() if key in Plan.model_fields.keys()}
            plan_data["hardware"] = HardwareRepository.get_hardware_from_record(record)
            return Plan(**plan_data)

    def get_plan_by_id(self, plan_id: int) -> Plan | None:
        query = """
            SELECT
                p.plan_id,
                p.plan_name,
                p.price,
                p.billing_period,
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
            FROM
                plans p
                LEFT JOIN extended_hardwares h using(hardware_id)
            WHERE
                p.plan_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (plan_id,))
                result = cursor.fetchone()

        return self.get_plan_from_record(result)

    def get_plan_by_name(self, plan_name: str) -> Plan | None:
        query = """
            SELECT
                p.plan_id,
                p.plan_name,
                p.price,
                p.billing_period,
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
            FROM
                plans p
                LEFT JOIN extended_hardwares h using(hardware_id)
            WHERE
                p.plan_name = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (plan_name,))
                result = cursor.fetchone()

        return self.get_plan_from_record(result)

    def get_plans(self) -> list[Plan]:
        query = """
            SELECT
                p.plan_id,
                p.plan_name,
                p.price,
                p.billing_period,
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
            FROM
                plans p
                LEFT JOIN extended_hardwares h using(hardware_id)
            ORDER BY p.plan_id;
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return [plan for plan in (self.get_plan_from_record(record) for record in result) if plan is not None]

    def get_available_plans_by_country(self, country: str) -> list[Plan]:
        query = """
            SELECT
                plan_id,
                plan_name,
                price,
                billing_period,
                hardware_id,
                cpu_id,
                cpu_name,
                cpu_vendor,
                cores,
                frequency,
                cpus_count,
                gpu_id,
                gpu_name,
                gpu_vendor,
                vram_type,
                vram_gb,
                gpus_count,
                storage_tb,
                ram_gb,
                bandwidth_gbps
            FROM available_plans_with_countries
            WHERE country = %s
            ORDER BY plan_id
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (country,))
                result = cursor.fetchall()

        return [plan for plan in (self.get_plan_from_record(record) for record in result) if plan is not None]
