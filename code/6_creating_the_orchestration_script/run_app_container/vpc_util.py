# Imports
import boto3
import time




# Constants
# This dictionary contains the IPv4 CIDRs for the VPC & the subnets
IPv4_CIDRS = {
    'VPC': '15.0.0.0/16',
    'PUBLIC_SUBNET': '15.0.1.0/24',
    'PRIVATE_SUBNET_1': '15.0.2.0/24',
    'PRIVATE_SUBNET_2': '15.0.3.0/24'
}




# Functions
# This function returns the Subnet ID
def get_subnet_id(name_tag, cidr, ec2_client):
    response = ec2_client.describe_subnets(Filters = [{'Name': 'cidr', 'Values': [cidr]}, {'Name': 'tag:Name', 'Values': [name_tag]}])
    #print(response)
    return response['Subnets'][0]['SubnetId']


# This function checks if a VPC exists. It returns True if the VPC is found, else returns False.
def check_if_vpc_exists(name_tag, cidr, ec2_client):
    response = ec2_client.describe_vpcs(Filters = [{'Name': 'cidr', 'Values': [cidr]}, {'Name': 'tag:Name', 'Values': [name_tag]}])
    return False if len(response['Vpcs']) == 0 else True


# This function checks if a Subnet exists. It returns True if the Subnet is found, else returns False.
def check_if_subnet_exists(name_tag, cidr, ec2_client):
    response = ec2_client.describe_subnets(Filters = [{'Name': 'cidr', 'Values': [cidr]}, {'Name': 'tag:Name', 'Values': [name_tag]}])
    return False if len(response['Subnets']) == 0 else True


# This function check if an Internet Gateway exists. It returns True if the Internet Gateway is found, else returns False.
def check_if_internet_gateway_exists(name_tag, ec2_client):
    response = ec2_client.describe_internet_gateways(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}])
    return False if len(response['InternetGateways']) == 0 else True


# This function checks if a NAT Gateway exists. It returns True if the NAT Gateway is found, else returns False.
def check_if_nat_gateway_exists(name_tag, ec2_client):
    response = ec2_client.describe_nat_gateways(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}, {'Name': 'state', 'Values': ['available', 'pending']}])
    return False if len(response['NatGateways']) == 0 else True


# This function check if a Route Table exists. It returns True if the Route Table is found, else returns False.
def check_if_route_table_exists(name_tag, ec2_client):
    response = ec2_client.describe_route_tables(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}])
    return False if len(response['RouteTables']) == 0 else True


# This function check if an Elastic IP exists. It returns True if the Elastic IP is found, else returns False.
def check_if_elastic_ip_exists(name_tag, ec2_client):
    response = ec2_client.describe_addresses(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}])
    return False if len(response['Addresses']) == 0 else True


# This function creates the VPC and returns its ID
def create_vpc(ec2_client, vpc_cidr, name_tag, **other_tags):
    vpc_tags = [{'Key': 'Name', 'Value': name_tag}]
    vpc_tags.extend([{'Key': tag_name, 'Value': tag_value} for tag_name, tag_value in other_tags.items()])
    response = ec2_client.create_vpc(
        DryRun = False,
        AmazonProvidedIpv6CidrBlock = False,
        InstanceTenancy = 'default',
        CidrBlock = vpc_cidr,
        TagSpecifications = [{'ResourceType': 'vpc', 'Tags': vpc_tags}]
    )
    #print(response)
    return response['Vpc']['VpcId']


# This function creates the Subnet and returns its ID
def create_subnet(ec2_client, vpc_id, subnet_cidr, name_tag, **other_tags):
    subnet_tags = [{'Key': 'Name', 'Value': name_tag}]
    subnet_tags.extend([{'Key': tag_name, 'Value': tag_value} for tag_name, tag_value in other_tags.items()])
    response = ec2_client.create_subnet(
            DryRun = False,
            VpcId = vpc_id,
            CidrBlock = subnet_cidr,
            TagSpecifications = [{'ResourceType': 'subnet', 'Tags': subnet_tags}]
    )
    #print(response)
    return response['Subnet']['SubnetId']


# This function creates the Internet Gateway and returns its ID
def create_internet_gateway(ec2_client, vpc_id, name_tag, **other_tags):
    igw_tags = [{'Key': 'Name', 'Value': name_tag}]
    igw_tags.extend([{'Key': tag_name, 'Value': tag_value} for tag_name, tag_value in other_tags.items()])
    response = ec2_client.create_internet_gateway(
        DryRun = False,
        TagSpecifications = [{'ResourceType': 'internet-gateway', 'Tags': igw_tags}]
    )
    #print(response)
    igw_id = response['InternetGateway']['InternetGatewayId']
    response = ec2_client.attach_internet_gateway(DryRun = False, InternetGatewayId = igw_id, VpcId = vpc_id)
    #print(response)
    return igw_id


# This function creates the Route Table and returns its ID
def create_route_table(ec2_client, vpc_id, subnet_ids, gateway_type, gateway_id, name_tag, **other_tags):
    rtbl_tags = [{'Key': 'Name', 'Value': name_tag}]
    rtbl_tags.extend([{'Key': tag_name, 'Value': tag_value} for tag_name, tag_value in other_tags.items()])
    response = ec2_client.create_route_table(
        DryRun = False,
        VpcId = vpc_id,
        TagSpecifications = [{'ResourceType': 'route-table', 'Tags': rtbl_tags}]
    )
    #print(response)
    rtbl_id = response['RouteTable']['RouteTableId']
    if gateway_type == 'INTERNET_GATEWAY':
        response = ec2_client.create_route(DryRun = False, RouteTableId = rtbl_id, DestinationCidrBlock = '0.0.0.0/0', GatewayId = gateway_id)
    elif gateway_type == 'NAT_GATEWAY':
        response = ec2_client.create_route(DryRun = False, RouteTableId = rtbl_id, DestinationCidrBlock = '0.0.0.0/0', NatGatewayId = gateway_id)
    else:
        print('Aborting execution !!!', 'ERROR')
        raise Exception('The specified gateway type is not supported')
    #print(response)
    for subnet_id in subnet_ids:
        response = ec2_client.associate_route_table(DryRun = False, RouteTableId = rtbl_id, SubnetId = subnet_id)
        #print(response)
    return rtbl_id


# This function creates the Elastic IP and returns its ID
def create_elastic_ip(ec2_client, name_tag, **other_tags):
    eip_tags = [{'Key': 'Name', 'Value': name_tag}]
    eip_tags.extend([{'Key': tag_name, 'Value': tag_value} for tag_name, tag_value in other_tags.items()])
    response = ec2_client.allocate_address(
        DryRun = False,
        Domain = 'vpc',
        TagSpecifications = [{'ResourceType': 'elastic-ip', 'Tags': eip_tags}]
    )
    #print(response)
    return response['AllocationId']


# This function creates the NAT Gateway and returns its ID
def create_natgateway(ec2_client, eip_id, subnet_id, name_tag, **other_tags):
    natgw_tags = [{'Key': 'Name', 'Value': name_tag}]
    natgw_tags.extend([{'Key': tag_name, 'Value': tag_value} for tag_name, tag_value in other_tags.items()])
    response = ec2_client.create_nat_gateway(
        DryRun = False,
        ConnectivityType = 'public',
        SubnetId = subnet_id,
        AllocationId = eip_id,
        TagSpecifications = [{'ResourceType': 'natgateway', 'Tags': natgw_tags}]
    )
    #print(response)
    natgw_id = response['NatGateway']['NatGatewayId']
    counter = 0
    while True:
        counter += 1
        response = ec2_client.describe_nat_gateways(NatGatewayIds=[natgw_id])
        #print(response)
        if counter > 40:
            print('Aborting execution !!!', 'ERROR')
            raise  Exception('Failed to start the NAT gateway')
        elif response['NatGateways'][0]['State'] == 'failed':
            print('Aborting execution !!!', 'ERROR')
            print(response)
            raise  Exception('Failed to start the NAT gateway')
        elif response['NatGateways'][0]['State'] == 'pending':
            print('Waiting for the NAT gateway to start...')
            time.sleep(60)
        elif response['NatGateways'][0]['State'] == 'available':
            break
        else:
            continue
    return natgw_id


# This function deletes the NAT gateway and returns its ID
def delete_nat_gateway(ec2_client, name_tag):
    response = ec2_client.describe_nat_gateways(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}, {'Name': 'state', 'Values': ['available']}])
    #print(response)
    natgw_id = response['NatGateways'][0]['NatGatewayId']
    response = ec2_client.delete_nat_gateway(DryRun = False, NatGatewayId = natgw_id)
    #print(response)
    counter = 0
    while True:
        counter += 1
        response = ec2_client.describe_nat_gateways(NatGatewayIds=[natgw_id])
        #print(response)
        if counter > 40:
            print('Aborting execution !!!', 'ERROR')
            raise  Exception('Failed to delete the NAT gateway')
        elif response['NatGateways'][0]['State'] == 'failed':
            print('Aborting execution !!!', 'ERROR')
            print(response)
            raise  Exception('Failed to delete the NAT gateway')
        elif response['NatGateways'][0]['State'] == 'deleting':
            print('Deleting the NAT gateway...')
            time.sleep(60)
        elif response['NatGateways'][0]['State'] == 'deleted':
            break
        else:
            continue
    return natgw_id


# This function deletes the Elastic IP and returns its ID
def delete_elastic_ip(ec2_client, name_tag):
    response = ec2_client.describe_addresses(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}])
    #print(response)
    allocation_id = response['Addresses'][0]['AllocationId']
    response = ec2_client.release_address(AllocationId = allocation_id, DryRun = False)
    #print(response)
    return allocation_id


# This function deletes the Subnet and returns its ID
def delete_subnet(ec2_client, cidr, name_tag):
    subnet_id = get_subnet_id(name_tag, cidr, ec2_client)
    response = ec2_client.delete_subnet(SubnetId = subnet_id, DryRun = False)
    #print(response)
    return subnet_id


# This function deletes the Route Table and returns its ID
def delete_route_table(ec2_client, name_tag):
    response = ec2_client.describe_route_tables(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}])
    #print(response)
    rtbl_id = response['RouteTables'][0]['RouteTableId']
    response = ec2_client.delete_route_table(DryRun = False, RouteTableId = rtbl_id)
    #print(response)
    return rtbl_id


# This function deletes the main Rote Table and returns its ID
def delete_main_route_table(ec2_client, vpc_cidr, vpc_name_tag):
    response = ec2_client.describe_vpcs(Filters = [{'Name': 'cidr', 'Values': [vpc_cidr]}, {'Name': 'tag:Name', 'Values': [vpc_name_tag]}])
    #print(response)
    vpc_id = response['Vpcs'][0]['VpcId']
    response = ec2_client.describe_route_tables(Filters = [{'Name': 'vpc-id', 'Values': [vpc_id]}])
    #print(response)
    rtbl_id = response['RouteTables'][0]['RouteTableId']
    response = ec2_client.delete_route_table(DryRun = False, RouteTableId = rtbl_id)
    #print(response)
    return rtbl_id


# This function deletes the Internet Gateway and returns its ID
def delete_internet_gateway(ec2_client, name_tag):
    response = ec2_client.describe_internet_gateways(Filters = [{'Name': 'tag:Name', 'Values': [name_tag]}])
    #print(response)
    igw_id = response['InternetGateways'][0]['InternetGatewayId']
    vpc_id = response['InternetGateways'][0]['Attachments'][0]['VpcId']
    response = ec2_client.detach_internet_gateway(DryRun = False, InternetGatewayId = igw_id, VpcId = vpc_id)
    #print(response)
    response = ec2_client.delete_internet_gateway(DryRun = False, InternetGatewayId = igw_id)
    #print(response)
    return igw_id


# This function deleted the VPC and returns its ID
def delete_vpc(ec2_client, cidr, name_tag):
    response = ec2_client.describe_vpcs(Filters = [{'Name': 'cidr', 'Values': [cidr]}, {'Name': 'tag:Name', 'Values': [name_tag]}])
    #print(response)
    vpc_id = response['Vpcs'][0]['VpcId']
    response = ec2_client.delete_vpc(VpcId = vpc_id, DryRun = False)
    #print(response)
    return vpc_id


# This function creates & configures the VPC service.
def setup_vpc(ec2_client, service_name_tags, **other_tags):
    # This dictionary contains the IDs of all the services managed by this code
    service_ids = {f'{key}':None for key in service_name_tags.keys()}

    # Checking to see if the vpc, subnets, eip, nat gateway, internet gateway, route tables exist
    print('Checking to see if the VPC, Subnets, Internet Gatway, NAT Gateway, Route Tables, and Elastic IP exist')
    for service, name_tag in service_name_tags.items():
        if 'VPC' in service:
            exists_flag = check_if_vpc_exists(name_tag, IPv4_CIDRS[service], ec2_client)
        elif 'SUBNET' in service:
            exists_flag = check_if_subnet_exists(name_tag, IPv4_CIDRS[service], ec2_client)
        elif 'INTERNET_GATEWAY' in service:
            exists_flag = check_if_internet_gateway_exists(name_tag, ec2_client)
        elif 'ROUTE_TABLE' in service:
            exists_flag = check_if_route_table_exists(name_tag, ec2_client)
        elif 'ELASTIC_IP' in service:
            exists_flag = check_if_elastic_ip_exists(name_tag, ec2_client)
        elif 'NAT_GATEWAY' in service:
            exists_flag = check_if_nat_gateway_exists(name_tag, ec2_client)
        else:
            continue
        if not exists_flag:
            print(f'The {name_tag} {service} does not exist.')
        else:
            print('Aborting execution !!!', 'ERROR')
            raise Exception(f'The {service} exists.')

    # Setting up the vpc, subnets, eip, nat gateway, internet gateway, route tables
    print('Setting up the VPC, Subnets, Internet Gatway, NAT Gateway, Route Tables, and Elastic IP')
    
    # Setting up the vpc
    service_ids['VPC'] = create_vpc(ec2_client, IPv4_CIDRS['VPC'], service_name_tags['VPC'], **other_tags)
    print(f"The {service_name_tags['VPC']} VPC has been created! The VPC ID is: {service_ids['VPC']}")
    
    # Setting up the subnets
    for service, name_tag, cidr in [(key, service_name_tags[key], IPv4_CIDRS[key]) for key in service_name_tags if 'SUBNET' in key]:
        service_ids[service] = create_subnet(ec2_client, service_ids['VPC'], cidr, name_tag, **other_tags)
        print(f'The {name_tag} Subnet has been created! The Subnet ID is: {service_ids[service]}')
    
    # Setting up the Internet Gateway
    service_ids['INTERNET_GATEWAY'] = create_internet_gateway(ec2_client, service_ids['VPC'], service_name_tags['INTERNET_GATEWAY'], **other_tags)
    print(f"The {service_name_tags['INTERNET_GATEWAY']} Internet Gateway has been created! The Internet Gateway ID is: {service_ids['INTERNET_GATEWAY']}")
    
    # Setting up the public Route Table
    service_ids['PUBLIC_ROUTE_TABLE'] = create_route_table(ec2_client, service_ids['VPC'], [service_ids['PUBLIC_SUBNET']], 'INTERNET_GATEWAY', service_ids['INTERNET_GATEWAY'], service_name_tags['PUBLIC_ROUTE_TABLE'], **other_tags)
    print(f"The {service_name_tags['PUBLIC_ROUTE_TABLE']} public Route Table has been created! The Route Table ID is: {service_ids['PUBLIC_ROUTE_TABLE']}")
    
    # Setting up the Elastic IP
    service_ids['ELASTIC_IP'] = create_elastic_ip(ec2_client, service_name_tags['ELASTIC_IP'], **other_tags)
    print(f"The {service_name_tags['ELASTIC_IP']} Elastic IP has been created! The Allocation ID is: {service_ids['ELASTIC_IP']}")
    
    # Setting up the NAT Gateway
    service_ids['NAT_GATEWAY'] = create_natgateway(ec2_client, service_ids['ELASTIC_IP'], service_ids['PUBLIC_SUBNET'], service_name_tags['NAT_GATEWAY'], **other_tags)
    print(f"The {service_name_tags['NAT_GATEWAY']} NAT Gateway has been created! The NAT Gateway ID is: {service_ids['NAT_GATEWAY']}")
    
    # Setting up the private public Route Table
    service_ids['PRIVATE_ROUTE_TABLE'] = create_route_table(ec2_client, service_ids['VPC'], [service_ids['PRIVATE_SUBNET_1'], service_ids['PRIVATE_SUBNET_2']], 'NAT_GATEWAY', service_ids['NAT_GATEWAY'], service_name_tags['PRIVATE_ROUTE_TABLE'], **other_tags)
    print(f"The {service_name_tags['PRIVATE_ROUTE_TABLE']} private Route Table has been created! The Route Table ID is: {service_ids['PRIVATE_ROUTE_TABLE']}")

    return service_ids


# This function tears down the VPC service.
def teardown_vpc(ec2_client, service_name_tags):
    # Checking to see if the vpc, subnets, eip, nat gateway, internet gateway, route tables exist
    print('Checking to see if the VPC, Subnets, Internet Gatway, NAT Gateway, Route Tables, and Elastic IP exist')
    for service, name_tag in service_name_tags.items():
        if 'VPC' in service:
            exists_flag = check_if_vpc_exists(name_tag, IPv4_CIDRS[service], ec2_client)
        elif 'SUBNET' in service:
            exists_flag = check_if_subnet_exists(name_tag, IPv4_CIDRS[service], ec2_client)
        elif 'INTERNET_GATEWAY' in service:
            exists_flag = check_if_internet_gateway_exists(name_tag, ec2_client)
        elif 'ROUTE_TABLE' in service:
            exists_flag = check_if_route_table_exists(name_tag, ec2_client)
        elif 'ELASTIC_IP' in service:
            exists_flag = check_if_elastic_ip_exists(name_tag, ec2_client)
        elif 'NAT_GATEWAY' in service:
            exists_flag = check_if_nat_gateway_exists(name_tag, ec2_client)
        else:
            continue
        if exists_flag:
            print(f'The {name_tag} {service} exists.')
        else:
            print('Aborting execution !!!', 'ERROR')
            raise Exception(f'The {service} does not exist.')

    # Deleting the NAT Gateway
    natgw_id = delete_nat_gateway(ec2_client, service_name_tags['NAT_GATEWAY'])
    print(f"The {service_name_tags['NAT_GATEWAY']} NAT Gateway (id: {natgw_id}) has been deleted")

    # Deleting the Elastic IP
    eip_allocation_id = delete_elastic_ip(ec2_client, service_name_tags['ELASTIC_IP'])
    print(f"The {service_name_tags['ELASTIC_IP']} Elastic IP (id: {eip_allocation_id}) has been deleted")

    # Deleting the Subnets
    for service, name_tag, cidr in [(key, service_name_tags[key], IPv4_CIDRS[key]) for key in service_name_tags if 'SUBNET' in key]:
        subnet_id = delete_subnet(ec2_client, cidr, name_tag)
        print(f"The {name_tag} {service} (id: {subnet_id}) has been deleted")

    # Deleting the Route Table
    for service, name_tag in [(key, service_name_tags[key]) for key in service_name_tags if 'ROUTE_TABLE' in key]:
        rtbl_id = delete_route_table(ec2_client, name_tag)
        print(f"The {name_tag} {service} (id: {rtbl_id}) has been deleted")

    # Deleting the Internet Gateway
    igw_id = delete_internet_gateway(ec2_client, service_name_tags['INTERNET_GATEWAY'])
    print(f"The {service_name_tags['INTERNET_GATEWAY']} Internet Gateway (id: {igw_id}) has been deleted")

    # Deleting the VPC
    vpc_id = delete_vpc(ec2_client, IPv4_CIDRS['VPC'], service_name_tags['VPC'])
    print(f"The {service_name_tags['VPC']} VPC (id: {vpc_id}) has been deleted")
