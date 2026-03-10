# EntraID (Azure AD) SAML Configuration Guide

This guide explains how to acquire the necessary `SAML2_METADATA_URL` to configure `django-saml2-auth` with Microsoft EntraID and set up the required local security binaries.

## Step 0: Install xmlsec1 (Windows Only)
SAML 2.0 requires the `xmlsec1` library for signing and verifying assertions.
1. Download the latest Windows 64-bit zip (e.g., `xmlsec1-1.3.9-win64.zip`) from the [official releases](https://github.com/lsh123/xmlsec/releases).
2. Extract the archive into a folder named `xmlsec1` in your project root.
3. The project's `settings.py` is pre-configured to automatically add `xmlsec1/xmlsec/bin/` to your system PATH at runtime.

## Step 1: Create an Enterprise Application in EntraID
1. Navigate to the **Microsoft Entra admin center**.
2. Go to **Identity** > **Applications** > **Enterprise applications**.
3. Select **New application** -> **Create your own application**.
4. Name the application (e.g., `ImA TODO`) and select "Integrate any other application you don't find in the gallery (Non-gallery)".
5. Click **Create**.

## Step 2: Configure Single Sign-On (SSO)
1. On the application overview page, select **Single sign-on** from the left-hand menu.
2. Select **SAML** as the Single Sign-On method.

### Basic SAML Configuration
1. Click **Edit** on the `Basic SAML Configuration` section.
2. **Identifier (Entity ID)**: Set this to match your Django app's ACS URL or a custom identifier (e.g., `https://yourdomain.com/saml2_auth/acs/`).
3. **Reply URL (Assertion Consumer Service URL)**: This MUST be the exact URL where SAML assertions will be sent.
   - For local testing: `http://127.0.0.1:8000/saml2_auth/acs/`
   - For production: `https://yourdomain.com/saml2_auth/acs/`
4. Click **Save**.

### User Attributes & Claims
By default, EntraID sends the `User.PrincipalName` as the NameID. You can map claims here to align with what `django-saml2-auth` expects (e.g., `email`, `givenname`, `surname`).

## Step 3: Get the App Federation Metadata URL
1. Scroll down to **Step 3: SAML Certificates**.
2. Find the field labeled **App Federation Metadata Url**.
3. Click the copy icon to copy this URL.
   It generally looks like: `https://login.microsoftonline.com/{Tenant_ID}/federationmetadata/2007-06/federationmetadata.xml?appid={App_ID}`

## Step 4: Download the SAML Signing Certificate
1. On the same **SAML Certificates** section, find **Certificate (Base64)**.
2. Click **Download** to save the certificate file (e.g., `Federation_Cert.cer`).
3. Optionally, also download the **Federation Metadata XML** file and save it (e.g., `Federation_File.xml`).
4. Place both files in your project directory (or a path of your choosing).
5. Open the `.env` file and set the paths relative to the project root:

```env
SAML2_METADATA_LOCAL_FILE_PATH=Federation_File.xml
SAML2_CERT_FILE=Federation_Cert.cer
```

> **Note:** If you only use the metadata URL (Step 3), the local metadata file is not strictly required. However, the certificate file is needed for signature verification.

## Step 5: Add the Metadata URL to `.env`
1. Open the `.env` file in the root of your Django project.
2. Paste the URL you copied in Step 3 into the `SAML2_METADATA_URL` variable.

```env
SAML2_METADATA_URL=https://login.microsoftonline.com/.../federationmetadata.xml?appid=...
```

Your Django application is now configured to fetch the SAML configuration dynamically from EntraID.
