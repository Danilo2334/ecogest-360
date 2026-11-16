import csv
import io
import json
from django.http import HttpResponse


def safe(value):
    text = str(value)
    if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(
        ("\t", "\r", "\n")
    ):
        return "'" + text
    return text


def export(context, rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    columns = [
        "row_type",
        "id",
        "date",
        "area",
        "material",
        "provenance",
        "generated",
        "verified_compost",
        "unit",
        "cutoff",
        "filters",
        "limitations",
    ]
    writer.writerow(columns)
    export_rows = rows or [
        {
            "row_type": "metadata",
            "id": "",
            "date": "",
            "area": "",
            "material": "",
            "provenance": context["provenance"],
            "generated": "0.000",
            "verified_compost": "0.000",
        }
    ]
    for row in export_rows:
        merged = {
            "row_type": "generation",
            **row,
            "unit": "kg",
            "cutoff": context["cutoff"],
            "filters": json.dumps(context["filters"], ensure_ascii=False),
            "limitations": context["limitations"],
        }
        writer.writerow([safe(merged[k]) for k in columns])
    response = HttpResponse(
        "\ufeff" + stream.getvalue(), content_type="text/csv; charset=utf-8"
    )
    response["Content-Disposition"] = 'attachment; filename="ecogest-generacion.csv"'
    response["X-Report-Cutoff"] = context["cutoff"]
    return response
