import argparse
import yaml
from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent / "templates" / "deployment_template.yaml"

def load_template():
    with open(TEMPLATE_PATH) as f:
        return yaml.safe_load(f)

def generate_deployment_yaml(app_name, image, ports):
    template = load_template()
    template["metadata"]["name"] = app_name
    template["spec"]["template"]["metadata"]["labels"]["app"] = app_name
    template["spec"]["selector"]["matchLabels"]["app"] = app_name
    template["spec"]["template"]["spec"]["containers"][0]["name"] = app_name
    template["spec"]["template"]["spec"]["containers"][0]["image"] = image
    template["spec"]["template"]["spec"]["containers"][0]["ports"] = [{"containerPort": p} for p in ports]
    return template

def save_yaml(content, output_file):
    with open(output_file, "w") as f:
        yaml.dump(content, f)
    print(f"Deployment YAML saved for {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate Kubernetes Deployment YAML")
    parser.add_argument("--app", required=True, help="Application name")
    parser.add_argument("--image", required=True, help="Docker image")
    parser.add_argument("--ports", nargs="+", type=int, required=True, help="list of container ports")
    parser.add_argument("--output", default="deployment.yaml", help="Output YAML file name")

    args = parser.parse_args()
    deployment_yaml = generate_deployment_yaml(args.app, args.image, args.ports)
    save_yaml(deployment_yaml, args.output)

if __name__ == "__main__":
    main()
