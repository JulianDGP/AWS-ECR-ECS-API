from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    CfnOutput,
)
from constructs import Construct

class CdkInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Crear una VPC con subredes públicas y sin NAT Gateways
        vpc = ec2.Vpc(self, "MyVpc",
            max_azs=1,  # Usamos una sola zona de disponibilidad para reducir recursos
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
            ]
        )   

        # Crear un cluster ECS en la VPC
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        # Referenciar el repositorio de ECR
        repository = ecr.Repository.from_repository_name(
            self, "ECRRepo", repository_name="julian/ecrtest"
        )

        # Definir la imagen del contenedor desde ECR
        container_image = ecs.ContainerImage.from_ecr_repository(repository, tag="latest")

        # Crear una definición de tarea
        task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
            cpu=256,
            memory_limit_mib=512,
        )

        # Añadir el contenedor a la tarea
        container = task_definition.add_container("WebContainer",
            image=container_image,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="MyFargateService"),
        )

        # Mapear el puerto del contenedor
        container.add_port_mappings(
            ecs.PortMapping(container_port=5000),
        )

        # Crear un Security Group que permita el trafico en el puerto 5000
        security_group = ec2.SecurityGroup(self, "FargateServiceSG",
            vpc=vpc,
            description="Permitir trafico HTTP entrante",
            allow_all_outbound=True,
        )

        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(5000),
            "Permitir trafico HTTP entrante en el puerto 5000",
        )

        # Crear el servicio Fargate sin Load Balancer
        fargate_service = ecs.FargateService(self, "MyFargateService",
            cluster=cluster,
            task_definition=task_definition,
            assign_public_ip=True,
            security_groups=[security_group],
            desired_count=1,
        )

        # No podemos obtener directamente la IP pública de la tarea en CDK,
        # pero podemos mostrar el nombre del cluster como salida
        CfnOutput(self, "ClusterName", value=cluster.cluster_name)
