from exchanges.serializers import ExchangeSerializer
from rest_framework import serializers
from rest_framework.fields import DurationField as DrfDurationField
from rest_framework.serializers import FloatField

from .models import AssetRecord, Robot


class DurationField(DrfDurationField):
    def to_representation(self, value):
        days = value.days
        seconds = value.seconds
        hours = seconds // 3600
        return f"{days}天{hours}小时"


class PercentageField(FloatField):
    def to_representation(self, value):
        result = super().to_representation(value)
        return "{:.2f}%".format(result * 100)


class AssetRecordSerializer(serializers.ModelSerializer):
    total_pnl_abs = serializers.FloatField(read_only=True)
    total_pnl_abs_24h = serializers.FloatField(read_only=True)
    total_pnl_rel_ptg = PercentageField(source="total_pnl_rel", read_only=True)
    total_pnl_rel_ptg_24h = PercentageField(source="total_pnl_rel_24h", read_only=True)

    class Meta:
        model = AssetRecord
        fields = [
            "currency",
            "total_principal",
            "total_balance",
            "total_pnl_abs",
            "total_pnl_abs_24h",
            "total_pnl_rel_ptg",
            "total_pnl_rel_ptg_24h",
        ]
        read_only_fields = [
            "currency",
            "total_principal_24h_ago",
            "total_balance_24h_ago",
            "robot",
        ]


class RobotListSerializer(serializers.ModelSerializer):
    duration_display = DurationField(source="duration", read_only=True)
    strategy_name = serializers.CharField(read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)

    class Meta:
        model = Robot
        fields = [
            # plain model fields
            "id",
            "name",
            "pair",
            "market_type",
            "enabled",
            "start_time",
            "ping_time",
            "target_currency",
            "base_currency",
            "quote_currency",
            "created_at",
            "modified_at",
            # related model fields
            "asset_record",
            # derived fields
            "duration_display",
            "strategy_name",
            "exchange",
        ]


class RobotRetrieveSerializer(serializers.ModelSerializer):
    duration_display = DurationField(source="duration", read_only=True)
    asset_record = AssetRecordSerializer(read_only=True)
    exchange = ExchangeSerializer(source="credential.exchange", read_only=True)

    class Meta:
        model = Robot
        fields = [
            # plain model fields
            "id",
            "name",
            "pair",
            "market_type",
            "enabled",
            "start_time",
            "ping_time",
            "target_currency",
            "base_currency",
            "quote_currency",
            "strategy_parameters",
            "created_at",
            "modified_at",
            # related fields
            "asset_record",
            # derived fields
            "duration_display",
            "strategy_spec_view",
            "exchange",
        ]


class RobotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "pair",
            "market_type",
            "target_currency",
            "base_currency",
            "quote_currency",
            "credential",
            "strategy",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "modified_at",
        ]


class RobotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
        ]
