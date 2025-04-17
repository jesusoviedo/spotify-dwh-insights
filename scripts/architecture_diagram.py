from diagrams import Cluster, Diagram  # type: ignore
from diagrams.custom import Custom  # type: ignore
from diagrams.gcp.analytics import BigQuery  # type: ignore
from diagrams.gcp.compute import ComputeEngine  # type: ignore
from diagrams.gcp.storage import GCS  # type: ignore
from diagrams.onprem.ci import GithubActions  # type: ignore
from diagrams.onprem.client import Users  # type: ignore
from diagrams.onprem.container import Docker  # type: ignore
from diagrams.onprem.iac import Terraform  # type: ignore
from diagrams.onprem.vcs import Github  # type: ignore

graph_attr = {"splines": "curved", "pad": "1.0", "nodesep": "1.0", "ranksep": "1.0"}

with Diagram(
    show=False, outformat=["png"], filename="resources/architecture_diagram", direction="LR", graph_attr=graph_attr
):

    api_spotify = Custom("API", "spotify.png")

    with Cluster("", graph_attr={"bgcolor": "transparent", "style": "dashed", "fontsize": "10"}):
        terraform = Terraform()

        with Cluster("", graph_attr={"bgcolor": "#e3f2fd", "style": "solid", "fontsize": "10"}):
            Custom("", "gcp.png")

            with Cluster(
                "Data Warehouse and Data Visualization", graph_attr={"bgcolor": "transparent", "style": "dashed"}
            ):
                bq = BigQuery("BigQuery")
                looker = Custom("Looker Studio", "looker.png")

            with Cluster("Data Lake", graph_attr={"bgcolor": "transparent", "style": "dashed"}):
                gcs = GCS("GCS")

            with Cluster("", graph_attr={"bgcolor": "#f0f0f0", "style": "solid", "fontsize": "10"}):
                compute = ComputeEngine("Compute Engine")

                with Cluster("", graph_attr={"bgcolor": "#e3eaf2", "style": "dashed"}):
                    docker_1 = Docker("")

                    with Cluster("", graph_attr={"bgcolor": "#ede7f6", "style": "solid", "fontsize": "10"}):
                        kestra = Custom("Kestra", "kestra.png")

                        with Cluster("transformation", graph_attr={"bgcolor": "transparent", "style": "dashed"}):
                            Custom("", "cron.png")
                            with Cluster("", graph_attr={"bgcolor": "transparent"}):
                                docker_1 = Docker("")
                                dbt = Custom("", "dbt.png")

                        with Cluster("ingestion", graph_attr={"bgcolor": "transparent", "style": "dashed"}):
                            Custom("", "cron.png")
                            with Cluster("", graph_attr={"bgcolor": "transparent"}):
                                docker_2 = Docker("")
                                dlt = Custom("", "dlt.png")

    with Cluster("Insights Consumer", graph_attr={"bgcolor": "#f0f4c3", "style": "solid", "fontsize": "10"}):
        user = Users("Business User")

    with Cluster("GitHub", graph_attr={"bgcolor": "#e3eaf2", "style": "solid", "fontsize": "10"}):
        github = Github("Source Code")
        with Cluster("", graph_attr={"bgcolor": "transparent", "style": "dashed"}):
            github_actions = GithubActions("GitHub Actions")

    with Cluster("GCP"):
        Custom("", "gcp.png")
        with Cluster("Terraform State Storage", graph_attr={"bgcolor": "transparent", "style": "dashed"}):
            gcs_terraform = GCS("GCS")

    api_spotify >> docker_2
    docker_2 << api_spotify
    docker_2 >> dlt
    dlt << docker_2

    dlt >> gcs
    gcs << dlt
    dlt >> bq

    dbt >> docker_1
    dbt << docker_1
    docker_1 >> bq
    docker_1 << bq

    bq >> looker
    looker << bq
    user >> looker

    terraform >> gcs_terraform

    github >> github_actions
    github_actions >> terraform
    github_actions >> compute
    github_actions >> kestra
