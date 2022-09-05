# Lacework CloudFormation Template Bulk Move of Lacework Accounts

![Lacework](https://user-images.githubusercontent.com/6440106/152378397-90c862e9-19fb-4427-96d0-02ca6c87f4dd.png)

## Overview
This CloudFormation can be used to move AWS accounts between Lacework tenant/sub-accounts in bulk. This move occurs on the Lacework
side only and does no impact the accounts on the AWS side. Simply specify the source and destination Lacework tenant/sub-account
and then optionally specify the list of AWS accounts to move. Leave the list of AWS accounts blank to move all of the accounts.

### Deploy the CloudFormation Template

1. Click on the following Launch Stack button to go to your CloudFormation console and launch the AWS Control Integration template.

   [![Launch](https://user-images.githubusercontent.com/6440106/153987820-e1f32423-1e69-416d-8bca-2ee3a1e85df1.png)](https://console.aws.amazon.com/cloudformation/home?#/stacks/create/review?templateURL=https://lacework-alliances.s3.us-west-2.amazonaws.com/lacework-tenant-move-accounts-cfn/templates/tenant-move-accounts.template.yml)

   For most deployments, you only need the Basic Configuration parameters.
   ![basic_configuration](https://user-images.githubusercontent.com/6440106/188283661-2cb114f6-724c-43d3-a3fa-a09911a20f03.png)
Specify the following Basic Configuration parameters:
   * Enter a **Stack name** for the stack.
   * Enter **Your Lacework URL**.
   * Enter your **Lacework Access Key ID** and **Secret Key** that you copied from your previous API Keys file.
   * Enter the **From Lacework Tenant/Sub-account Name** that currently has the accounts.
   * Enter the **To Lacework Tenant/Sub-account Name** where you want to move the accounts to.
   * Enter the **AWS Accounts** as a comma-separated list of AWS Accounts IDs or leave blank to move all of the accounts.
   ![sub_account_configuration](https://user-images.githubusercontent.com/6440106/154780411-50b270b5-4246-4e12-acb1-b1d4997b5671.png)
3. Click **Next** through to your stack **Review**.
4. Accept the AWS CloudFormation terms and click **Create stack**.



